import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter
from pivLib import read_piv
from skimage import io, draw, filters
from corrLib import divide_windows, readdata
import trackpy as tp
from scipy.ndimage import gaussian_filter1d
from fit_circle_utils import fit_circle
import matplotlib.patches as mpatch
# %% codecell
def tangent_unit(point, center):
    """Compute tangent unit vector based on point coords and center coords.
    Args:
    point -- 2-tuple
    center -- 2-tuple
    Returns:
    tu -- tangent unit vector
    """
    point = np.array(point)
    # center = np.array(center)
    r = np.array((point[0] - center[0], point[1] - center[1]))
    # the following two lines set the initial value for the x of the tangent vector
    ind = np.logical_or(r[1] > 0, np.logical_and(r[1] == 0, r[0] > 0))
    x1 = np.ones(point.shape[1:])
    x1[ind] = -1
    y1 = np.zeros(point.shape[1:])
    x1[(r[1]==0)] = 0
    y1[(r[1]==0)&(r[0]>0)] = -1
    y1[(r[1]==0)&(r[0]<0)] = 1

    y1[r[1]!=0] = np.divide(x1 * r[0], r[1], where=r[1]!=0)[r[1]!=0]
    length = (x1**2 + y1**2) ** 0.5
    return np.divide(np.array([x1, y1]), length, out=np.zeros_like(np.array([x1, y1])), where=length!=0)

def intersection(lst1, lst2):
    """
    Return the intersection of two lists.
    """
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def fit_for_outer_drop_z(a, b, r, ri, traj):
    """
    Assume inner droplets are always sliding on the surface of outer droplets.
    Find the z position with the least net deviation of trajectories from the surface.

    Args:
    a -- x coordinate of outer drop center
    b -- y coordinate of outer drop center
    r -- outer drop radius
    ri -- inner drop radius
    traj -- xyz-traj.csv DataFrame

    Returns:
    c -- z coordinate of outer drop center
    """
    err = 1e9
    for c_temp in np.linspace(0, r): # this assumes the real center lies in(0, r)
        dx = traj.x - a; dy = traj.y - b; dz = traj.z - c_temp
        temp_err = (((dx**2 + dy**2 + dz**2)**0.5 - (r-ri))**2).sum()
        plt.scatter(c_temp, temp_err)
        if err > temp_err:
            err = temp_err
            c = c_temp
    plt.scatter(c, err, s=100, marker='x', c='red')

    return float(c)

def plot_traj_overlay(traj, img):
    """Plot particle trajectory on the initial frame of an image sequence
    This function visualize the strength of fluctuation relative to the confinement size

    Args:
    traj -- DataFrame comprising columns x and y
    img -- an array like image

    Returns:
    fig -- the figure object
    """
    fig = plt.figure(figsize=(3, 3/img.shape[1]*img.shape[0]), dpi=300)
    ax = fig.add_axes([0,0,1,1])
    ax.imshow(img, cmap='gray')
    ax.axis('off')
    ax.scatter(traj.x, traj.y, s=0.7, c=np.arange(len(traj))/len(traj))
    plt.close()
    return fig

def center_traj(log_entry, folder):
    '''load trajectory and shift trajectory to a coordinate system with origin at the top of outer droplet
    This function assumes inner droplets are always sliding on the outer surfaces.
    Z positions are calculated based on xy positions.'''
    R = log_entry[('analysis', 'OD')] / 2
    r = log_entry[('analysis', 'ID')] / 2
    a = log_entry[('analysis', 'a')]
    b = log_entry[('analysis', 'b')]
    traj = load_xyz_traj(log_entry, folder)
    traj['x'] = traj['x'] - a
    traj['y'] = traj['y'] - b
    traj['z'] = R - r - ((R-r)**2 - traj['x']**2 - traj['y']**2) ** 0.5
    return traj

def r3(x, a):
    return a * x ** 3

def load_xyz_traj(log_entry, folder):
    '''Use log entry to load trajectory data from xyz-traj.csv'''
    date = '{:08d}'.format(log_entry[('params', 'Date')])
    subfolder = log_entry[('params', 'Subfolder')]
    traj_dir = os.path.join(folder, date, subfolder, 'crop_HoughCircles', 'xyz-traj.csv')
    if os.path.exists(traj_dir):
        return pd.read_csv(traj_dir)
    else:
        print('Data not found')

# wrap the subpixel correction in a function
def subpixel_correction_(original_circle, raw_img, range_factor=0.6, plot=True, thres=10, method="gaussian"):
    """Use gaussian fitting of cross-boundary pixel intensities to give circle detections subpixel accuracy. 
    Args:
    original_circle -- dict of {"x", "y", "r"}
    raw_img -- raw image where circles are detected
    range_factor -- the range of the cross-boundary pixel intensity profile to be fitted.
                    For example, 0.6 means 0.6*r on both sides of the boundary pixel (in and out of the circle, 1.2*r in total)".
    Returns:
    corrected_circle -- dict of {"x", "y", "r"}
    Edit:
    06152022 -- Initial commit.
    06162022 -- If the peak value is too far away from the original one, drop it.
    06172022 -- 1) add boundary protection,
                2) use gaussian smoothing, instead of savgol
                3) convert pixel data type to "float64" to avoid memory overflow
                4) put fitting part together
                5) merge gaussian and minimum fitting in the same function, adding "method" argument, change name to subpixel_correction
    06212022 -- Deprecated. Use a more compact sampling code.
    """
    def minimal_x(x, y):
        """Get the x corresponds to minimal y.
        Args:
        x, y -- 1D arrays of same shape
        Returns:
        x_min -- x corresponds to minimal y
        """
        assert(x.shape==y.shape)
        ind = np.argsort(y)
        x_min = x[ind[0]]
        y_min = y[ind[0]]
        return x_min, y_min
    
    x0, y0, r0 = original_circle["x"], original_circle["y"], original_circle["r"]
    xdata = {}
    ydata = {}
    original_points = {"up": (x0, y0-r0),
                       "down": (x0, y0+r0),
                       "left": (x0-r0, y0),
                       "right": (x0+r0, y0)}
    new_points = {}
    init_map = {"up": 1,
               "down": 1,
               "left": 0,
               "right": 0}
    p = {}
    
    # get cross-boundary intensity profile 1 (up)
    p1_r0 = max(int(np.round(y0 - r0 - r0*range_factor)), 0)
    p1_r1 = min(int(np.round(y0 - r0 + r0*range_factor)), raw_img.shape[0])
    p1_c = int(np.round(x0))
    p["up"] = raw_img[p1_r0:p1_r1, p1_c].astype("float64")
    # Fit the curve with Gaussian
    xdata["up"] = np.arange(p1_r0, p1_r1)
    
    # get cross-boundary intensity profile 2 (down)
    p2_r0 = max(int(np.round(y0 + r0 - r0*range_factor)), 0)
    p2_r1 = min(int(np.round(y0 + r0 + r0*range_factor)), raw_img.shape[0])
    p2_c = int(np.round(x0))
    p["down"] = raw_img[p2_r0:p2_r1, p2_c].astype("float64")
    # Fit the curve with Gaussian
    xdata["down"] = np.arange(p2_r0, p2_r1)
        
    # get cross-boundary intensity profile 3 (left)
    p3_r = int(np.round(y0))
    p3_c0 = max(int(np.round(x0-r0-r0*range_factor)), 0)
    p3_c1 = min(int(np.round(x0-r0+r0*range_factor)), raw_img.shape[1])
    p["left"] = raw_img[p3_r, p3_c0:p3_c1].astype("float64")
    # Fit the curve with Gaussian
    xdata["left"] = np.arange(p3_c0, p3_c1)
        
    # get cross-boundary intensity profile 4 (right)
    p4_r = int(np.round(y0))
    p4_c0 = max(int(np.round(x0+r0-r0*2/3)), 0)
    p4_c1 = min(int(np.round(x0+r0+r0*2/3)), raw_img.shape[1])
    p["right"] = raw_img[p4_r, p4_c0:p4_c1].astype("float64")
    # Fit the curve with Gaussian
    xdata["right"] = np.arange(p4_c0, p4_c1)
    
    if plot:
        count = 1
        fig = plt.figure(figsize=(8, 8)) 
        plt.tight_layout()
        
    for kw in p:
        ydata[kw] = gaussian_filter1d(p[kw], sigma=r0/10/4)
        if method == "gaussian":
            popt, pcov = curve_fit(gauss1, xdata[kw], ydata[kw], 
                                                     p0=[ydata[kw].min()-ydata[kw].max(), original_points[kw][init_map[kw]], 5, ydata[kw].mean()])
            new_coord = popt[1]            
        elif method == "minimum":
            xc, yc = minimal_x(xdata[kw], ydata[kw])
            new_coord = xc  
        
        if kw == "up" or kw == "down":
            new_points[kw] = (original_points[kw][0], new_coord)
        else:
            new_points[kw] = (new_coord, original_points[kw][1])
            
        if (new_points[kw][0]-original_points[kw][0])**2 \
            + (new_points[kw][0]-original_points[kw][0])**2 > thres**2:
            new_points[kw] = original_points[kw]
        
        # plot gaussian fitting
        if plot:                             
            ax = fig.add_subplot(2, 2, count)
            ax.plot(xdata[kw], p[kw], color="gray", label="raw")
            ax.plot(xdata[kw], ydata[kw], color="black", label="smooth")
            if method == "gaussian":
                ax.plot(xdata[kw], gauss1(xdata[kw], *popt), color="red", label="fit")
            elif method == "minimum":
                ax.scatter(xc, yc, s=50, color="red")
            ax.legend()
            ax.set_xlabel("r (px)")
            ax.set_ylabel("intensity")
            count += 1
            
    # fit circle
    point_list = []
    for kw in new_points:
        point_list.append(new_points[kw])
    xy = np.array(point_list)
    c = fit_circle(xy[:, 0], xy[:, 1])
    corrected_circle = {"x": c["a"], "y": c["b"], "r": c["r"]}
    
    return corrected_circle

# wrap the subpixel correction in a function
def subpixel_correction(original_circle, raw_img, range_factor=0.6, plot=True, thres=10, method="gaussian", sample=10):
    """Use gaussian fitting of cross-boundary pixel intensities to give circle detections subpixel accuracy. 
    Args:
    original_circle -- dict of {"x", "y", "r"}
    raw_img -- raw image where circles are detected
    range_factor -- the range of the cross-boundary pixel intensity profile to be fitted.
                    For example, 0.6 means 0.6*r on both sides of the boundary pixel (in and out of the circle, 1.2*r in total)".
    Returns:
    corrected_circle -- dict of {"x", "y", "r"}
    Edit:
    06152022 -- Initial commit.
    06162022 -- If the peak value is too far away from the original one, drop it.
    06172022 -- 1) add boundary protection,
                2) use gaussian smoothing, instead of savgol
                3) convert pixel data type to "float64" to avoid memory overflow
                4) put fitting part together
                5) merge gaussian and minimum fitting in the same function, adding "method" argument, change name to subpixel_correction
    06212022 -- Sample more profiles for more accurate correction.
                Note that sometimes more profiles does not mean more accuracy.
                If the outer droplet boundary is very dark, 
                and some profiles contain the outer droplet boundary,
                significant deviation will result. 
    """
    
    x0, y0, r0 = original_circle["x"], original_circle["y"], original_circle["r"]
    # samples
    new_points = []
    for t in np.linspace(0, 2*np.pi, sample, endpoint=False):
        xc = x0 + r0 * np.cos(t)
        yc = y0 + r0 * np.sin(t)
        x1 = xc - r0 * range_factor * np.cos(t)
        x2 = xc + r0 * range_factor * np.cos(t)
        y1 = yc - r0 * range_factor * np.sin(t)
        y2 = yc + r0 * range_factor * np.sin(t)
        x1 = int(np.round(x1))
        x2 = int(np.round(x2))
        y1 = int(np.round(y1))
        y2 = int(np.round(y2))
        y, x = draw.line(y1, x1, y2, x2)
        indx = (x >= 0) & (x < raw_img.shape[1])
        indy = (y >= 0) & (y < raw_img.shape[0])
        ind = indx * indy
        y = y[ind]
        x = x[ind]
        p = raw_img[y, x]
        p_smooth = gaussian_filter1d(p, sigma=3/4)
        if method == "minimum":
            minind = np.argmin(p_smooth)
            xmin, ymin = x[minind], y[minind]
            distsq = (xmin - xc) ** 2 + (ymin - yc) ** 2 
            if distsq > thres ** 2:
                new_points.append((xc, yc))
            else:
                new_points.append((xmin, ymin))
        elif method == "gaussian":
            raise ValueError("Method not yet implemented")
            
    # fit circle
    xy = np.array(new_points)
    c = fit_circle(xy[:, 0], xy[:, 1])
    corrected_circle = {"x": c["a"], "y": c["b"], "r": c["r"]}
    
    if plot == True:
        points = np.array(new_points)
        fig, ax = plt.subplots(dpi=150)
        ax.imshow(raw_img, cmap="gray")
        ax.scatter(points[:, 0], points[:, 1])
        
    return corrected_circle


# test function subpixel_correction_
# folder = r"C:\Users\liuzy\Documents\06022022"
# n = 2
# raw_img = io.imread(os.path.join(folder, "{:02d}".format(n), "00000.tif"))
# inner_traj = pd.read_csv(os.path.join(folder, "Analysis", "{:02d}".format(n), "t1.csv"))
# x0, y0, r0 = inner_traj.x.iloc[0], inner_traj.y.iloc[0], inner_traj.r.iloc[0]
# original_circle = {"x": x0, "y": y0, "r": r0}
# corrected_circle = subpixel_correction(original_circle, raw_img, range_factor=0.6, 
#                                          plot=True, thres=15, method="minimum", sample=4)
# fig = plt.figure(figsize=(3, 3), dpi=150)
# ax = fig.add_axes([0,0,1,1])
# ax.imshow(raw_img, cmap="gray")
# cobj = mpatch.Circle((original_circle["x"], original_circle["y"]), original_circle["r"], fill=False, ec="red", lw=1)
# ax.add_patch(cobj)
# ccor = mpatch.Circle((corrected_circle["x"], corrected_circle["y"]), corrected_circle["r"], fill=False, ec="yellow", lw=1)
# ax.add_patch(ccor)


def circle_quality_std(raw_img, circle, distsq_thres=10):
    """Quantify circle detection quality by computing boundary pixel standard deviation.
    Args:
    raw_img -- raw image
    circle -- dict of {"x", "y", "r"}
    distsq_thres -- distance threshold for determining if a pixel is on a circle or not
    Returns:
    quality -- 1 - (circle pixel std) / (image pixel std)
                The idea is to normalize the results from images of different contrast,
                and larger quality value means better tracking.                
    """
    x, y, r = circle["x"], circle["y"], circle["r"]
    # 1. make X, Y coordinates of all image pixels
    Y, X = np.mgrid[0:raw_img.shape[0], 0:raw_img.shape[1]]
    # 2. compute distance (square) matrix from each pixel to circle center
    dist = (X-x) ** 2 + (Y-y) ** 2 - r ** 2 
    # 3. make a boolean matrix ind where the distance is smaller than 5 (note that 5 is an arbitrary number and need revision)
    distsq_thres = 10
    ind = abs(dist) < distsq_thres
    # 4. use the ind matrix to get all the pixel intensity values on the detected circle
    circle_pixels = raw_img[ind]
    # 5. compute standard deviation of circle_pixels
    std = circle_pixels.std()
    std_img = raw_img.std()
    
    return 1 - std / std_img


# test circle_quality_std()
# folder = r"C:\Users\liuzy\Documents\06032022"
# n = 2
# frame = 5000
# raw_img = io.imread(os.path.join(folder, "{:02d}".format(n), "{:05d}.tif".format(frame)))
# inner_traj = pd.read_csv(os.path.join(folder, "Analysis", "{:02d}".format(n), "t1.csv")).set_index("frame")
# x0, y0, r0 = inner_traj.x.loc[frame], inner_traj.y.loc[frame], inner_traj.r.loc[frame]
# original_circle = {"x": x0, "y": y0, "r": r0}
# corrected_circle = subpixel_correction_gaussian(original_circle, raw_img, range_factor=0.6, plot=False)

# original_quality = circle_quality_std(raw_img, original_circle)
# corrected_quality = circle_quality_std(raw_img, corrected_circle)
# print("original quality: {:.2f}".format(original_quality))
# print("corrected quality: {:.2f}".format(corrected_quality))

def correct_traj(folder, n, filename, correction_params, save_step=100):    
    """work function of traj correction"""
    n = int(n)
    circle_list = []
    original_traj = pd.read_csv(os.path.join(folder, "Analysis", "{:02d}".format(n), 
                                             "{}.csv".format(filename)))
    original_traj.frame = original_traj.frame.astype("int")
    original_traj = original_traj.set_index("frame")
    n_frames = len(original_traj)
    count = 0
    analysis_folder = os.path.join(folder, "Analysis", "{:02d}".format(n))
    snapshot_folder = os.path.join(analysis_folder, "cropped{}c".format(filename))
    if os.path.exists(snapshot_folder) == False:
        os.makedirs(snapshot_folder)
    t0 = time.monotonic()
    for num, i in original_traj.iterrows():
        original_circle = {"x": i.x, "y": i.y, "r": i.r}
        raw_img = io.imread(os.path.join(folder, "{:02d}".format(n), "{:05d}.tif".format(num)))
        corrected_circle = subpixel_correction(original_circle, raw_img, **correction_params)
        original_quality = circle_quality_std(raw_img, original_circle)
        corrected_quality = circle_quality_std(raw_img, corrected_circle)
        corrected_circle["frame"] = num
        corrected_circle["original_quality"] = original_quality
        corrected_circle["corrected_quality"] = corrected_quality
        circle_list.append(pd.DataFrame(corrected_circle, index=[num]))

        fig = plt.figure(figsize=(3,3), dpi=100)
        ax = fig.add_axes([0,0,1,1])
        ax.imshow(raw_img, cmap="gray")
        cobj = mpatch.Circle((original_circle["x"], original_circle["y"]), original_circle["r"], fill=False, ec="red", lw=1)
        ax.add_patch(cobj)
        ccor = mpatch.Circle((corrected_circle["x"], corrected_circle["y"]), corrected_circle["r"], fill=False, ec="green", lw=1)
        ax.add_patch(ccor)
        ax.set_xlim([int(original_circle["x"]-original_circle["r"]-10), int(original_circle["x"]+original_circle["r"]+10)])
        ax.set_ylim([int(original_circle["y"]-original_circle["r"]-10), int(original_circle["y"]+original_circle["r"]+10)])
        ax.annotate(num, (0.5, 0.5), xycoords="axes fraction")    
        if count % save_step == 0:        
            fig.savefig(os.path.join(snapshot_folder, "{:05d}.jpg".format(num)))
        plt.pause(0.01)
        plt.close()
        show_progress(count / n_frames)
        t1 = time.monotonic()-t0
        print("time: {0:.1f} s | processing speed: {1:.1f} frame/s".format(t1, count/t1))
        clear_output(wait=True)    
        count += 1
    corrected_traj = pd.concat(circle_list)
    with open(os.path.join(analysis_folder, "correction_params{}c.json".format(filename)), "w") as f:
        f.write(json.dumps(correction_params))
    corrected_traj.to_csv(os.path.join(folder, "Analysis", "{:02d}".format(n), "{}c.csv".format(filename)))
    
def generate_correction_report(folder, n, filename):
    """working function for generating correction report"""
    traj_folder = os.path.join(folder, "Analysis", "{:02d}".format(n))
    original_traj = pd.read_csv(os.path.join(traj_folder, 
                                         "{}.csv".format(filename)))
    original_traj.frame = original_traj.frame.astype("int")
    original_traj = original_traj.set_index("frame")
    corrected_traj = pd.read_csv(os.path.join(traj_folder, 
                                              "{}c.csv".format(filename)))
    corrected_traj.frame = corrected_traj.frame.astype("int")
    corrected_traj = corrected_traj.set_index("frame")
    frame = corrected_traj.sample().index[0]
    raw_img = io.imread(os.path.join(folder, "{:02d}".format(n), "{:05d}.tif".format(frame)))

    fig = plt.figure(figsize=(9, 6), dpi=120)
    ax1 = fig.add_subplot(231)
    ax1.set_title("traj overview")
    ax1.imshow(raw_img, cmap="gray")
    ax1.scatter(original_traj.x, original_traj.y, color="red", s=1, alpha=0.5)
    ax1.scatter(corrected_traj.x, corrected_traj.y, color="green",s=1, alpha=0.5)

    ax2 = fig.add_subplot(232)
    ax2.set_title("traj zoom-in")
    ax2.scatter(original_traj.x, original_traj.y, color="red", alpha=0.5)
    ax2.scatter(corrected_traj.x, corrected_traj.y, color="green", alpha=0.5)

    ax3 = fig.add_subplot(233)
    ax3.set_title("x subpx bias")
    histx, bin_edges = np.histogram(original_traj.x - original_traj.x.apply(np.floor),
                                   bins=np.linspace(0, 1, 11))
    ax3.bar(bin_edges[:-1], histx, 
            align="edge", width=bin_edges[1]-bin_edges[0], 
            color="red", alpha=0.5, label="original")
    histx, bin_edges = np.histogram(corrected_traj.x - corrected_traj.x.apply(np.floor),
                                   bins=np.linspace(0, 1, 11))
    ax3.bar(bin_edges[:-1], histx, 
            align="edge", width=bin_edges[1]-bin_edges[0], 
            color="green", alpha=0.5, label="corrected")    
    
    ax4 = fig.add_subplot(234)
    ax4.set_title("y subpx bias")
    histx, bin_edges = np.histogram(original_traj.y - original_traj.y.apply(np.floor),
                                   bins=np.linspace(0, 1, 11))
    ax4.bar(bin_edges[:-1], histx, 
            align="edge", width=bin_edges[1]-bin_edges[0], 
            color="red", alpha=0.5, label="original")
    histx, bin_edges = np.histogram(corrected_traj.y - corrected_traj.y.apply(np.floor),
                                   bins=np.linspace(0, 1, 11))
    ax4.bar(bin_edges[:-1], histx, 
            align="edge", width=bin_edges[1]-bin_edges[0], 
            color="green", alpha=0.5, label="corrected")

    ax5 = fig.add_subplot(235)
    ax5.set_title("tracking quality")
    ax5.plot(corrected_traj.index, savgol_filter(corrected_traj.original_quality, 31, 2), color="red", label="original")
    ax5.plot(corrected_traj.index, savgol_filter(corrected_traj.corrected_quality, 31, 2), color="green", label="corrected")
    ax5.set_xlabel("frame")
    ax5.set_ylabel("quality")
    ax5.legend()

    ax6 = fig.add_subplot(236)
    ax6.set_title("random comparison")
    ax6.imshow(raw_img, cmap="gray")
    co = mpatch.Circle((original_traj.loc[frame].x, original_traj.loc[frame].y), original_traj.loc[frame].r,
                       fill=False, ec="red", lw=1) 
    cc = mpatch.Circle((corrected_traj.loc[frame].x, corrected_traj.loc[frame].y), corrected_traj.loc[frame].r,
                       fill=False, ec="green", lw=1)
    ax6.add_patch(co)
    ax6.add_patch(cc)
    roi_factor = 1.5
    ax6.set_xlim([original_traj.loc[frame].x - roi_factor*original_traj.loc[frame].r, original_traj.loc[frame].x + roi_factor*original_traj.loc[frame].r])
    ax6.set_ylim([original_traj.loc[frame].y - roi_factor*original_traj.loc[frame].r, original_traj.loc[frame].y + roi_factor*original_traj.loc[frame].r])
    ax6.annotate(frame, (0.5, 0.5), xycoords="axes fraction", horizontalalignment="center")
    plt.tight_layout()
    fig.savefig(os.path.join(traj_folder, "{}c-report.jpg".format(filename)))
    

# folder = r"C:\Users\liuzy\Documents\06012022"
# n = 1
# correction_params = {"range_factor": 0.2,
#                      "thres": 10,
#                      "method": "minimum",
#                      "plot": True}
# filename = "t0"
# correct_traj(folder, n, filename, correction_params)
# generate_correction_report(os.path.join(folder, "Analysis", "{:02}".format(n)), filename)