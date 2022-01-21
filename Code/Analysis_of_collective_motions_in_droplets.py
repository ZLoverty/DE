# This notebook make plots and demos for the note Analysis_of_collective_motions_in_droplets
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter
from pivLib import read_piv
from skimage import io
from corrLib import divide_windows, readdata
from de_utils import tangent_unit
# %% codecell
folder = r"C:\Users\liuzy\Documents\12092021"
mv_folder = os.path.join(folder, "mean_velocity")
v21 = pd.read_csv(os.path.join(mv_folder, "21.csv"))

v21.head()
plt.plot(v21.frame, v21.mean_v)
# velocity is too noisy, use savgol filter to smooth it
plt.plot(v21.frame, savgol_filter(v21.mean_v, 1001, 3))
# clearly, mean velocity drops from 20 px/s to 15 px/s
# the unit px/s translates to 0.16 um/s, i.e. 3.2 um/s to 2.4 um/s
# these values seem a little too small compared to my experience
# need to double check the videos to see if the values comprise any artifact

# %% codecell
v22 = pd.read_csv(os.path.join(mv_folder, "22.csv"))
v23 = pd.read_csv(os.path.join(mv_folder, "23.csv"))
v24 = pd.read_csv(os.path.join(mv_folder, "24.csv"))
v22.frame += 30000
v23.frame += 60000
v24.frame += 90000
plt.figure(dpi=150)
for v in [v21, v22, v23, v24]:
    plt.plot(v.frame/50, savgol_filter(v.mean_v, 3001, 3)*0.16)
plt.xlabel("time (s)")
plt.ylabel("$v$ (um/s)")
# 1. velocity decay is most pronounced in the first 10 min, later on the velocity remains constant for 30 min
# 2. Confocal measures a higher mean velocity
# 3. Confocal laser does not seem to harm bacterial activity
# 4. the sudden drop of velocity in the middle of yellow curve is not expected, watch video to find out why.

# %% codecell
# mean velocities
folder = r"C:\Users\liuzy\Documents\01052022"
l = readdata(folder, "csv")
t_offset = 0
plt.figure(figsize=(6, 3), dpi=150)
for num, i in l[:20].iterrows():
    mv = pd.read_csv(i.Dir)
    plt.plot((mv.frame+t_offset)/50/60, savgol_filter(mv.mean_v, 301, 3)*0.16, label=num)
    t_offset += mv.frame.iloc[-1]
plt.legend(bbox_to_anchor=(1,1), ncol=2, fontsize=5)
plt.xlabel("time (min)")
plt.ylabel("mean velocity (um/s)")
# mv.iloc[-1].frame

# pd.read_csv(l.loc[12].Dir).plot()
# pd.read_csv(l.loc[12].Dir).set_index("frame")[6500:6520].plot()
# %% codecell
# compute tangent normal
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
# %% codecell

t = np.linspace(0, 2*np.pi, 20)
point = (np.cos(t), np.sin(t))
# center = (np.zeros(len(t)), np.zeros(len(t)))
center = (0, 0)
tu = tangent_unit(point, center)
plt.quiver(point[0], point[1], tu[0], tu[1])
plt.axis('equal')
# %% codecell
point = (1, 1)
center = (0, 0)
tu = tangent_unit(point, center)
plt.quiver(point[0], point[1], 0.7, -0.7)
plt.quiver(point[0], point[1], -0.7, 0.7, color='red')
plt.axis('equal')
# %% codecell
x = np.linspace(-1, 1)
point = np.mgrid[-1:1:10j, -1:1:10j]
center = (0, 0)
tu = tangent_unit(point, center)
plt.quiver(point[0], point[1], tu[0], tu[1])
# plt.quiver(point[0], point[1], -0.7, 0.7, color='red')
plt.axis('equal')
# %% codecell
def order_parameter_wioland2013(pivData, center):
    """Compute order parameter with PIV data and droplet center coords using the method from wioland2013.
    Args:
    pivData -- DataFrame of x, y, u, v
    center -- 2-tuple droplet center coords
    Return:
    OP -- float, max to 1
    """
    pivData = pivData.dropna()
    point = (pivData.x, pivData.y)
    tu = tangent_unit(point, center)
    # \Sigma vt
    sum_vt = abs((pivData.u * tu[0] + pivData.v * tu[1])).sum()
    sum_v = ((pivData.u**2 + pivData.v**2) ** 0.5).sum()
    OP = (sum_vt/sum_v - 2/np.pi) / (1 - 2/np.pi)
    return OP


# %% codecell
from skimage import io
pivData = pd.read_csv(os.path.join("test_files", "00000-00001.csv")).dropna()
img = io.imread(os.path.join("test_files", "22.tif"))
center = (259, 228)
order_parameter_wioland2013(pivData, center)

# %% codecell
point = (pivData.x, pivData.y)
tu = tangent_unit(point, center)
plt.figure(dpi=150)
plt.imshow(img, cmap='gray')
plt.quiver(pivData.x, pivData.y, pivData.u, pivData.v, color='yellow', width=0.005)
plt.quiver(pivData.x, pivData.y, tu[0], tu[1], color='red', width=0.0025)
# plt.axis('off')

# %% codecell
plt.quiver(pivData.x, pivData.y, tu[0], tu[1], color='red', width=0.0025)

# %% codecell
# 12092021 - 22 and 24 order parameter
folder = r"C:\Users\liuzy\Documents\12092021\circulation_order_parameter"
data = pd.read_csv(os.path.join(folder, "22.csv"))
plt.plot(data.frame/50, savgol_filter(data.OP, 11, 3))
plt.xlabel("time (s)")
plt.ylabel("order parameter")

# %% codecell
winsize = 40
overlap = 20
maski = io.imread(os.path.join("test_files", "freehand_mask.tif")) > 0
mask = divide_windows(maski, windowsize=[winsize, winsize], step=winsize-overlap)[2] >= 1


x, y, u, v = read_piv(os.path.join("test_files", "06972-06973.csv"))
# xm = x * mask
# ym = y * mask
u[~mask] = np.nan
v[~mask] = np.nan
plt.imshow(maski)
plt.figure()
plt.imshow(maski*0, vmin=-1000, cmap='gray')
plt.quiver(x, y, um, vm, color='red', width=0.0025)
plt.figure()
plt.imshow(maski)
plt.quiver(x, y, u, v, color='red', width=0.0025)

# %% codecell
v = pd.read_csv(os.path.join("test_files", "zero_control.csv"))
plt.plot(v.frame/50, v.mean_v*0.16)
plt.xlabel("time (s)")
plt.ylabel("mean velocity (um/s)")
# %% codecell
def PIV_masked(I0, I1, winsize, overlap, dt, mask):
    """Apply PIV analysis on masked images
    Args:
    I0, I1 -- adjacent images in a sequence
    winsize, overlap, dt -- PIV parameters
    mask -- a boolean array, False marks masked region and True marks the region of interest
    mask_procedure -- the option chosen to apply the mask, used for testing, remove in the future.
    Returns:
    frame_data -- x, y, u, v DataFrame, here x, y is wrt original image, (u, v) are in px/s

    This function is rewritten based on the PIV_droplet() function in piv_droplet.py script.
    The intended usage is just to pass one additional `mask` parameter, on top of conventional parameter set.

    EDIT
    ====
    Dec 14, 2021 -- Initial commit.
    Dec 15, 2021 -- After testing 2 masking procedure, option 1 is better.
                    Two procedures produce similar results, but option 1 is faster.
                    So this function temporarily uses option 1, until a better procedure comes.

    MASKING PROCEDURE
    =================
    Option 1:
    i) Mask on raw image: I * mask, perform PIV
    ii) Divide mask into windows: mask_w
    iii) use mask_w to mask resulting velocity field: u[~mask_w] = np.nan
    ---
    Option 2:
    i) Perform PIV on raw images
    ii) Divide mask into windows:mask_w
    iii) use mask_w to mask resulting velocity field: u[~mask_w] = np.nan
    ---
    """
    assert(mask.shape==I0.shape)
    mask = mask >= mask.mean() # convert mask to boolean array
    I0_mask = I0 * mask
    I1_mask = I1 * mask
    x, y, u, v = PIV(I0_mask, I1_mask, winsize, overlap, dt)
    mask_w = divide_windows(mask, windowsize=[winsize, winsize], step=winsize-overlap)[2] >= 1
    assert(mask_w.shape==x.shape)
    u[~mask_w] = np.nan
    v[~mask_w] = np.nan
    return x, y, u, v
# %% codecell
# How to convert mask to mask_w (windowed mask)
mask = io.imread(os.path.join("test_files", "freehand_mask.tif"))
mask_binary = mask > mask.mean()
mask_w01 = divide_windows(mask_binary, windowsize=[winsize, winsize], step=winsize-overlap)[2] >= 0.1
mask_w05 = divide_windows(mask_binary, windowsize=[winsize, winsize], step=winsize-overlap)[2] >= 0.5
mask_w1 = divide_windows(mask_binary, windowsize=[winsize, winsize], step=winsize-overlap)[2] >= 1
fig, ax = plt.subplots(ncols=4, nrows=1, dpi=150)
for ax1, m, t in zip(ax, [mask_binary, mask_w01, mask_w05, mask_w1], ['mask', 'thre=0.1', 'thre=0.5', 'thre=1']):
    ax1.imshow(m)
    ax1.axis('off')
    ax1.set_title(t)
# %% codecell
for w in [40, 30, 20, 10]:
    print(r"python piv_drop.py D:\Github\DE\Code\test_files\raw_images D:\Github\DE\Code\test_files\w{0} {0} {1} 0.02 D:\Github\DE\Code\test_files\mask.tif".format(w, w//2))
# %% codecell
fig, axs = plt.subplots(nrows=2, ncols=5, dpi=200)
img = io.imread(os.path.join("test_files", "raw_images", "00000.tif"))
for w, ax in zip(range(10, 110, 10), axs.flatten()):
    overlap = w // 2
    piv = pd.read_csv(os.path.join("test_files", "w{0:d}_o{1:d}".format(w, overlap), "00000-00001.csv")).dropna()
    v = ((piv.u ** 2 + piv.v ** 2) ** 0.5).mean() * 0.16
    ax.imshow(img*0, vmin=-1000, cmap='gray')
    ax.quiver(piv.x, piv.y, piv.u, piv.v, scale_units="width", scale=900)
    ax.set_xlim([80, 440])
    ax.set_ylim([50, 410])
    ax.axis('off')
    ax.set_title("w={:d}".format(w))
    ax.text(130, 0, r"$\bar v=$ {:.2f} um/s".format(v), fontsize=6)
# %% codecell
fig, ax = plt.subplots(nrows=1, ncols=2, dpi=200, sharey=True)
for w in range(10, 110, 10):
    overlap = w // 2
    piv = pd.read_csv(os.path.join("test_files", "w{0:d}_o{1:d}".format(w, overlap), "00000-00001.csv")).dropna()
    hist, bin_edges = np.histogram(piv.u.dropna()*0.16, density=True, bins=np.linspace(-10, 10, 10))
    ax[0].plot(bin_edges[:-1], hist, label="w={:d}".format(w))
    hist, bin_edges = np.histogram(piv.v.dropna()*0.16, density=True, bins=np.linspace(-10, 10, 10))
    ax[1].plot(bin_edges[:-1], hist, label="w={:d}".format(w))
ax[0].set_xlabel("velocity (um/s)")
ax[0].set_ylabel("PDF")
ax[0].set_title("u distribution")
ax[1].set_xlabel("velocity (um/s)")
ax[1].set_ylabel("PDF")
ax[1].legend(fontsize=7)
ax[1].set_title("v distribution")
# %% codecell
fig, axs = plt.subplots(nrows=2, ncols=5, dpi=200)
img = io.imread(os.path.join("test_files", "raw_images", "00000.tif"))
for w, ax in zip(range(10, 110, 10), axs.flatten()):
    overlap = w - 5
    piv = pd.read_csv(os.path.join("test_files", "w{0:d}_o{1:d}".format(w, overlap), "00000-00001.csv")).dropna()
    v = ((piv.u ** 2 + piv.v ** 2) ** 0.5).mean() * 0.16
    ax.imshow(img*0, vmin=-1000, cmap='gray')
    ax.quiver(piv.x, piv.y, piv.u, piv.v, scale_units="width", scale=900)
    ax.set_xlim([80, 440])
    ax.set_ylim([50, 410])
    ax.axis('off')
    ax.set_title("w={:d}".format(w))
    ax.text(130, 0, r"$\bar v=$ {:.2f} um/s".format(v), fontsize=6)
# %% codecell
fig, ax = plt.subplots(nrows=1, ncols=2, dpi=200, sharey=True)
for w in range(10, 110, 10):
    overlap = w - 5
    piv = pd.read_csv(os.path.join("test_files", "w{0:d}_o{1:d}".format(w, overlap), "00000-00001.csv")).dropna()
    hist, bin_edges = np.histogram(piv.u.dropna()*0.16, density=True, bins=np.linspace(-10, 10, 10))
    ax[0].plot(bin_edges[:-1], hist, label="w={:d}".format(w))
    hist, bin_edges = np.histogram(piv.v.dropna()*0.16, density=True, bins=np.linspace(-10, 10, 10))
    ax[1].plot(bin_edges[:-1], hist, label="w={:d}".format(w))
ax[0].set_xlabel("velocity (um/s)")
ax[0].set_ylabel("PDF")
ax[0].set_title("u distribution")
ax[1].set_xlabel("velocity (um/s)")
ax[1].set_ylabel("PDF")
ax[1].legend(fontsize=7)
ax[1].set_title("v distribution")

# %% codecell
# mean velocity
for w in [10, 20, 30, 40, 50]:
    piv = pd.read_csv(os.path.join("test_files", "w{:d}".format(w), "00000-00001.csv")).dropna()
    v = ((piv.u ** 2 + piv.v ** 2) ** 0.5).mean()
    print("{0:d} | {1:.2f}".format(w, v))
# %% codecell
# order parameter
def order_parameter_wioland2013(pivData, center):
    """Compute order parameter with PIV data and droplet center coords using the method from wioland2013.
    Args:
    pivData -- DataFrame of x, y, u, v
    center -- 2-tuple droplet center coords
    Return:
    OP -- float, max to 1
    """
    point = (pivData.x, pivData.y)
    tu = tangent_unit(point, center)
    # \Sigma vt
    sum_vt = (pivData.u * tu[0] + pivData.v * tu[1]).sum()
    sum_v = ((pivData.u**2 + pivData.v**2) ** 0.5).sum()
    # OP = (sum_vt/sum_v - 2/np.pi) / (1 - 2/np.pi)
    OP = sum_vt/sum_v
    return OP
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
    # avoid divided by 0
    r[1][r[1]==0] = np.nan

    y1 = - x1 * r[0] / r[1]
    length = (x1**2 + y1**2) ** 0.5
    return np.array([x1, y1]) / length
# %% codecell
center = (259, 228)
for w in [10, 20, 30, 40, 50]:
    piv = pd.read_csv(os.path.join("test_files", "w{:d}".format(w), "00006-00007.csv"))
    OP = order_parameter_wioland2013(piv, center)
    print("{0:d} | {1:.2f}".format(w, OP))
# %% codecell
(17.9**2 + 41.2**2) ** 0.5
# %% codecell
# velocity profile
def velocity_profile_radial(pivData, center):
    """Compute radial velocity profile of PIV in droplet
    Args:
    pivData - DataFrame of x, y, u, v
    center - 2-tuple center of droplet
    Returns:
    vp - velocity profile, DataFrame of r, v_r
    """
    pivData = pivData.dropna()
    d = ((pivData.x - center[0]) ** 2 + (pivData.y - center[1]) ** 2) ** 0.5
    pivData = pivData.assign(d=d)
    # determine the range and interval of velocity profile
    N = 10 # number of points in the profile
    bin_edges = np.linspace(0, pivData.d.max(), N+1)
    v_list = []
    n_list = []
    for minn, maxx in zip(bin_edges[:-1], bin_edges[1:]):
        in_range = pivData.loc[(pivData.d>minn)&(pivData.d<=maxx)]
        n_list.append(len(in_range))
        v = ((in_range.u ** 2 + in_range.v ** 2) ** 0.5).mean()
        v_list.append(v)
    vp = pd.DataFrame({"r": bin_edges[1:], "v": v_list, "n": n_list})
    return vp
# %% codecell
for i in range(0, 10, 2):
    pivData = pd.read_csv(os.path.join("test_files", "w20_o10", "{0:05d}-{1:05d}.csv".format(i, i+1)))
    center = (259, 228)
    vp = velocity_profile_radial(pivData, center)
    plt.plot(vp.r*0.16, vp.v*0.16)
plt.xlabel("radius (um)")
plt.ylabel("mean velocity (um/s)")
plt.figure()
plt.plot(vp.r, vp.n)

# %% codecell
np.linspace(0, 10)
# %% codecell
# max velocity first 1000 data
piv_folder = r"C:\Users\liuzy\Documents\12092021\piv_drop\22"
l = readdata(piv_folder, "csv")
v_list = []
for num, i in l[1000:1200].iterrows():
    pivData = pd.read_csv(i.Dir).dropna()
    vmax = (pivData.u ** 2 + pivData.v ** 2).max() ** 0.5
    v_list.append(vmax)
plt.plot(v_list)
# %% codecell
# is the velocity field symmetric azimuthally?
# if so, we should have completely random azimuthal velocity profile
# otherwise, the azimuthal velocity profile would show some special distribution

# %% codecell
def velocity_profile_azimuthal(pivData, center):
    """Compute azimuthal velocity profile of PIV in droplet
    Args:
    pivData - DataFrame of x, y, u, v
    center - 2-tuple center of droplet
    Returns:
    vp - velocity profile, DataFrame of r, v_r
    """
    pivData = pivData.dropna()
    theta = np.arctan2(pivData.y - center[1], pivData.x - center[0])
    pivData = pivData.assign(theta=theta)
    # determine the range and interval of velocity profile
    N = 10 # number of points in the profile
    bin_edges = np.linspace(-np.pi, np.pi, N+1)
    interval = 2 * np.pi / N
    v_list = []
    n_list = []
    for t in bin_edges[:-1]:
        minn = t
        maxx = t + interval
        in_range = pivData.loc[(pivData.theta>minn)&(pivData.theta<=maxx)]
        n_list.append(len(in_range))
        v = ((in_range.u ** 2 + in_range.v ** 2) ** 0.5).mean()
        v_list.append(v)
    vp = pd.DataFrame({"theta": bin_edges[:-1], "v": v_list, "n": n_list})
    return vp
# %% codecell
pivData = pd.read_csv(os.path.join("test_files", "w20_o10", "{0:05d}-{1:05d}.csv".format(8, 9)))
center = (259, 228)
vp = velocity_profile_azimuthal(pivData, center)
plt.plot(vp.theta, vp.v)
# %% codecell
# plot polar chart
N = len(vp)
theta = np.linspace(-np.pi, np.pi, N, endpoint=False)
radii = vp.v * 0.16
width = 2 * np.pi / N
colors = plt.cm.viridis(radii / radii.max())
ax = plt.subplot(projection='polar')
ax.bar(theta, radii, width=width, bottom=0.0, color=colors, alpha=0.5)
# %% codecell
# test np.arctan2
t = np.linspace(-np.pi, np.pi)
y = np.sin(t)
x = np.cos(t)
theta = np.arctan2(y, x)
plt.plot(t, theta)
# %% codecell
# The bottom seem to have larger velocity always? Try a random frame
piv_folder = r"C:\Users\liuzy\Documents\12092021\piv_drop\22"
i = 11020
pivData = pd.read_csv(os.path.join(piv_folder, "{0:05d}-{1:05d}.csv".format(i, i+1)))
center = (259, 228)
vp = velocity_profile_azimuthal(pivData, center)
# %% codecell
N = len(vp)
theta = np.linspace(-np.pi, np.pi, N, endpoint=False)
radii = vp.v
width = 2 * np.pi / N
colors = plt.cm.viridis(radii / radii.max())
ax = plt.subplot(projection='polar')
ax.bar(theta, radii, width=width, bottom=0.0, color=colors, alpha=0.5)
# %% codecell
# Not always large at bottom, but seem to be some slower dynamics...
# Let's make a video to find out
piv_folder = r"C:\Users\liuzy\Documents\12092021\piv_drop\22"
save_folder = r"C:\Users\liuzy\Documents\12092021\azimuthal_profile"
l = readdata(piv_folder, "csv")
center = (259, 228)
for num, i in l.iterrows():
    pivData = pd.read_csv(i.Dir)
    vp = velocity_profile_azimuthal(pivData, center)
    N = len(vp)
    theta = np.linspace(-np.pi, np.pi, N, endpoint=False)
    radii = vp.v
    width = 2 * np.pi / N
    colors = plt.cm.viridis(radii / radii.max())
    ax = plt.subplot(projection='polar')
    ax.bar(theta, radii, width=width, bottom=0.0, color=colors, alpha=0.5)
    ax.set_ylim([0, 60])
    plt.savefig(os.path.join(save_folder, "{:05d}.jpg".format(num)))
    plt.close()
# %% codecell
dir(ax)
# %% codecell
string_list = ["a", "b", "c"]
" && ".join(string_list)
# %% codecell
piv_folder = r"C:\Users\liuzy\Documents\12092021\piv_drop\22"
l = readdata(piv_folder, "csv")
vp_list = []
for num, i in l.iterrows():
    pivData = pd.read_csv(i.Dir)
    center = (259, 228)
    vp = velocity_profile_radial(pivData, center).set_index("r")
    vp_list.append(vp)
vp_df = pd.concat(vp_list, axis=1)
vp_mean = vp_df.mean(axis=1).to_frame("v")
plt.plot(vp_mean.index*0.16, vp_mean.v*0.16)
plt.xlabel("radius (um)")
plt.ylabel("mean velocity (um/s)")
# %% codecell
piv_folder = r"C:\Users\liuzy\Documents\12092021\piv_drop\22"
l = readdata(piv_folder, "csv")
vp_list = []
for num, i in l.iterrows():
    pivData = pd.read_csv(i.Dir)
    center = (259, 228)
    vp = velocity_profile_azimuthal(pivData, center).set_index("theta")
    vp_list.append(vp)
vp_df = pd.concat(vp_list, axis=1)
vp_mean = vp_df["v"].mean(axis=1).to_frame("v")

N = len(vp_mean)
theta = np.linspace(-np.pi, np.pi, N, endpoint=False)
radii = vp_mean.v
width = 2 * np.pi / N
colors = plt.cm.viridis(radii / radii.max())
ax = plt.subplot(projection='polar')
ax.bar(theta, radii, width=width, bottom=0.0, color=colors, alpha=0.5)
# %% codecell
vp_df["v"].T.reset_index()

vp_df["v"].T.reset_index()[:300].drop(columns="index").plot()
plt.legend()
# %% codecell
def azimuthal_velocity_profile_radial(pivData, center):
    """Compute radial velocity profile of azimuthal velocity from PIV in droplet
    Args:
    pivData - DataFrame of x, y, u, v
    center - 2-tuple center of droplet
    Returns:
    vp - velocity profile, DataFrame of r, v_r
    """
    pivData = pivData.dropna()
    tu = tangent_unit((pivData.x, pivData.y), center)
    d = ((pivData.x - center[0]) ** 2 + (pivData.y - center[1]) ** 2) ** 0.5
    pivData = pivData.assign(d=d, tu=tu[0], tv=tu[1])
    # determine the range and interval of velocity profile
    N = 10 # number of points in the profile
    bin_edges = np.linspace(0, pivData.d.max(), N+1)
    v_list = []
    n_list = []
    for minn, maxx in zip(bin_edges[:-1], bin_edges[1:]):
        in_range = pivData.loc[(pivData.d>minn)&(pivData.d<=maxx)]
        n_list.append(len(in_range))
        v = (in_range.tu * in_range.u + in_range.tv * in_range.v).mean()
        v_list.append(v)
    vp = pd.DataFrame({"r": bin_edges[1:], "v": v_list, "n": n_list})
    return vp
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
    x1 = - np.ones(point.shape[1:])
    x1[ind] = 1
    # avoid divided by 0
    r[1][r[1]==0] = np.nan

    y1 = x1 * r[0] / r[1]
    length = (x1**2 + y1**2) ** 0.5
    return np.array([x1, y1]) / length
# %% codecell
pivData = pd.read_csv(os.path.join("test_files", "00000-00001.csv"))
center = (259, 228)
point = (pivData.x, pivData.y)
tu = tangent_unit(point, center)
# %% codecell
plt.figure(dpi=150)
plt.quiver(point[0], point[1], tu[0], tu[1])
# %% codecell
for i in range(0, 10, 2):
    pivData = pd.read_csv(os.path.join("test_files", "w20_o10", "{0:05d}-{1:05d}.csv".format(i, i+1)))
    center = (259, 228)
    vp = azimuthal_velocity_profile_radial(pivData, center)
    plt.plot(vp.r*0.16, vp.v*0.16)
plt.xlabel("r (um)")
plt.ylabel("azimuthal velocity (um/s)")
# %% codecell
folder = r"C:\Users\liuzy\Documents\12092021\piv_drop\22"
center = (259, 228)
l = readdata(folder, "csv")
vp_list = []
for num, i in l.iterrows():
    pivData = pd.read_csv(i.Dir)
    vp = azimuthal_velocity_profile_radial(pivData, center)
    vp_list.append(vp.set_index("r")["v"])
vp_df = pd.concat(vp_list, axis=1)
vp_mean = vp_df.mean(axis=1).to_frame("v")
plt.plot(vp_mean.index*0.16, vp_mean.v*0.16)
plt.xlabel("r (um)")
plt.ylabel("azimuthal velocity (um/s)")
# %% codecell
def azimuthal_velocity_profile_azimuthal(pivData, center):
    """Compute azimuthal velocity profile of azimuthal velocity from PIV in droplet
    Args:
    pivData - DataFrame of x, y, u, v
    center - 2-tuple center of droplet
    Returns:
    vp - velocity profile, DataFrame of r, v_r
    """
    pivData = pivData.dropna()
    tu = tangent_unit((pivData.x, pivData.y), center)
    theta = np.arctan2(pivData.y - center[1], pivData.x - center[0])
    pivData = pivData.assign(theta=theta, tu=tu[0], tv=tu[1])
    # determine the range and interval of velocity profile
    N = 10 # number of points in the profile
    bin_edges = np.linspace(-np.pi, np.pi, N+1)
    interval = 2 * np.pi / N
    v_list = []
    n_list = []
    for t in bin_edges[:-1]:
        minn = t
        maxx = t + interval
        in_range = pivData.loc[(pivData.theta>minn)&(pivData.theta<=maxx)]
        n_list.append(len(in_range))
        v = (in_range.u * in_range.tu + in_range.v * in_range.tv).mean()
        v_list.append(v)
    vp = pd.DataFrame({"theta": bin_edges[:-1], "v": v_list, "n": n_list})
    return vp
# %% codecell
piv_folder = r"C:\Users\liuzy\Documents\12092021\piv_drop\22"
l = readdata(piv_folder, "csv")
vp_list = []
for num, i in l.iterrows():
    pivData = pd.read_csv(i.Dir)
    center = (259, 228)
    vp = azimuthal_velocity_profile_azimuthal(pivData, center).set_index("theta")
    vp_list.append(vp)
vp_df = pd.concat(vp_list, axis=1)
vp_mean = vp_df["v"].mean(axis=1).to_frame("v")

N = len(vp_mean)
theta = np.linspace(-np.pi, np.pi, N, endpoint=False)
radii = vp_mean.v
width = 2 * np.pi / N
colors = plt.cm.viridis(radii / radii.max())
ax = plt.subplot(projection='polar')
ax.bar(theta, radii, width=width, bottom=0.0, color=colors, alpha=0.5)
# %% codecell
def order_parameter_hamby2018(pivData, center):
    """Computes order parameter using the definition in Hamby 2018.
    Args:
    pivData - DataFrame of x, y, u, v
    center - 2-tuple center of droplet
    Returns:
    OP - order parameter
    """
    pivData = pivData.dropna()
    tu = tangent_unit((pivData.x, pivData.y), center)
    pivData = pivData.assign(tu=tu[0], tv=tu[1])
    OP = (pivData.u * pivData.tu + pivData.v * pivData.tv).sum() / ((pivData.u ** 2 + pivData.v ** 2) ** 0.5).sum()
    return OP
# %% codecell
pivData = pd.read_csv(os.path.join("test_files", "00000-00001.csv")).dropna()
center = (259, 228)
order_parameter_hamby2018(pivData, center)
# %% codecell
plt.figure(dpi=250)
img = io.imread(os.path.join("test_files", "22.tif"))
plt.imshow(img, cmap='gray')
tu = tangent_unit((pivData.x, pivData.y), center)
plt.quiver(pivData.x, pivData.y, pivData.u, pivData.v, color="yellow", width=0.004)
plt.quiver(pivData.x, pivData.y, tu[0], tu[1], color="red", width=0.0015)
# plt.axis("off")
# %% codecell
folder = r"C:\Users\liuzy\Documents\12092021\piv_drop\22"
l = readdata(folder, "csv")
OP_list = []
frame_list = []
for num, i in l[:3000].iterrows():
    pivData = pd.read_csv(i.Dir).dropna()
    OP = order_parameter_hamby2018(pivData, center)
    frame = int(i.Name.split("-")[0])
    frame_list.append(frame)
    OP_list.append(OP)
plt.figure(dpi=100)
plt.plot(np.array(frame_list)/50, savgol_filter(np.array(OP_list), 11, 3))
plt.xlabel("time (s)")
plt.ylabel("$\psi$")
# %% codecell
# investigate the coordinate system issue
# a 3x3 velocity field going clockwise
x = np.array([[0, 1, 2], [0, 1, 2], [0, 1, 2]])
y = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
u = np.array([[1, 1, 0], [0, 0, 0], [0, -1, -1]])
v = np.array([[0, 0, 1], [-1, 0, 1], [-1, 0, 0]])
# %% codecell
# quiver synthetic PIV
plt.imshow(np.random.rand(3, 3), vmin=-1000, cmap='gray')
plt.quiver(x, y, u, v)
# %% codecell
x = np.array([[0, 1, 2], [0, 1, 2], [0, 1, 2]])
y = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
u = np.array([[1, 1, 0], [0, 0, 0], [0, -1, -1]])
v = np.array([[0, 0, -1], [-1, 0, 1], [-1, 0, 0]])
plt.imshow(np.random.rand(3, 3), vmin=-1000, cmap='gray')
# plt.quiver(x, y, u, v)
tu = tangent_unit((x, y), (1, 1))
plt.quiver(x, y, tu[0], tu[1], color="red")

# %% codecell
piv_folder = r"C:\Users\liuzy\Documents\12092021\piv_drop\22"
center = (259, 228)
l = readdata(piv_folder, "csv")
plt.figure(dpi=150)
for num, i in l[::2200].iterrows():
    vp_tmp = []
    for j in range(50):
        pivData = pd.read_csv(l.loc[num+j].Dir)
        vp_tmp.append(velocity_profile_radial(pivData, center).set_index("r")["v"])
    vp = pd.concat(vp_tmp, axis=1).mean(axis=1).to_frame("v")
    plt.plot(vp.index*0.16, vp.v*0.16, label=num/25)

piv_folder = r"C:\Users\liuzy\Documents\12092021\piv_drop\22"
center = (259, 228)
l = readdata(piv_folder, "csv")
vp_tmp = []
for num, i in l[::2200].iterrows():
    pivData = pd.read_csv(i.Dir)
    vp_tmp.append(velocity_profile_radial(pivData, center).set_index("r")["v"])
vp = pd.concat(vp_tmp, axis=1).mean(axis=1).to_frame("v")
plt.plot(vp.index*0.16, vp.v*0.16, color="black", lw=3, label="mean")
plt.legend(fontsize=7)
plt.xlabel("r (um)")
plt.ylabel("velocity (um/s)")
# %% codecell
piv_folder = r"C:\Users\liuzy\Documents\12092021\piv_drop\22"
center = (259, 228)
l = readdata(piv_folder, "csv")
plt.figure(dpi=150)
for num, i in l[::2200].iterrows():
    vp_tmp = []
    for j in range(50):
        pivData = pd.read_csv(l.loc[num+j].Dir)
        vp_tmp.append(azimuthal_velocity_profile_radial(pivData, center).set_index("r")["v"])
    vp = pd.concat(vp_tmp, axis=1).mean(axis=1).to_frame("v")
    plt.plot(vp.index*0.16, vp.v*0.16, label=num/25)

piv_folder = r"C:\Users\liuzy\Documents\12092021\piv_drop\22"
center = (259, 228)
l = readdata(piv_folder, "csv")
vp_tmp = []
for num, i in l[::2200].iterrows():
    pivData = pd.read_csv(i.Dir)
    vp_tmp.append(azimuthal_velocity_profile_radial(pivData, center).set_index("r")["v"])
vp = pd.concat(vp_tmp, axis=1).mean(axis=1).to_frame("v")
plt.plot(vp.index*0.16, vp.v*0.16, color="black", lw=3, label="mean")
plt.legend(fontsize=7)
plt.xlabel("r (um)")
plt.ylabel("velocity (um/s)")
# %% codecell
# 12 - center - (405, 382)
# 13 - center - (422, 400)
piv_folder = r"E:\01052022\piv_drop\12"
center = (405, 382)
l = readdata(piv_folder, "csv")
vp_tmp = []
plt.figure()
for num, i in l[::500].iterrows():
    pivData = pd.read_csv(i.Dir)
    vp_tmp.append(velocity_profile_radial(pivData, center).set_index("r")["v"])
vp = pd.concat(vp_tmp, axis=1).mean(axis=1).to_frame("v")
plt.plot(vp.index*0.16, vp.v*0.16, color="black", lw=3, label="xz")

piv_folder = r"E:\01052022\piv_drop\13"
center = (422, 400)
l = readdata(piv_folder, "csv")
vp_tmp = []
for num, i in l[::500].iterrows():
    pivData = pd.read_csv(i.Dir)
    vp_tmp.append(velocity_profile_radial(pivData, center).set_index("r")["v"])
vp = pd.concat(vp_tmp, axis=1).mean(axis=1).to_frame("v")
plt.plot(vp.index*0.16, vp.v*0.16, color="red", lw=3, label="xy")
plt.legend(fontsize=15)
plt.xlabel("r (um)")
plt.ylabel("velocity (um/s)")
# %% codecell
# azimuthal
piv_folder = r"E:\01052022\piv_drop\12"
center = (405, 382)
l = readdata(piv_folder, "csv")
vp_tmp = []
plt.figure()
for num, i in l[::100].iterrows():
    pivData = pd.read_csv(i.Dir)
    vp_tmp.append(azimuthal_velocity_profile_radial(pivData, center).set_index("r")["v"])
vp = pd.concat(vp_tmp, axis=1).mean(axis=1).to_frame("v")
plt.plot(vp.index*0.16, vp.v*0.16, color="black", lw=3, label="xz")

piv_folder = r"E:\01052022\piv_drop\13"
center = (422, 400)
l = readdata(piv_folder, "csv")
vp_tmp = []
for num, i in l[::100].iterrows():
    pivData = pd.read_csv(i.Dir)
    vp_tmp.append(azimuthal_velocity_profile_radial(pivData, center).set_index("r")["v"])
vp = pd.concat(vp_tmp, axis=1).mean(axis=1).to_frame("v")
plt.plot(vp.index*0.16, vp.v*0.16, color="red", lw=3, label="xy")
plt.legend(fontsize=15)
plt.xlabel("r (um)")
plt.ylabel("velocity (um/s)")
# %% codecell
# mean velocity evolution - use 01052022 sample 3 as an example
meanv_list = []
for n in range(0, 18):
    piv_folder = r"E:\01052022\piv_drop\{:02d}".format(n)
    l = readdata(piv_folder, "csv")
    v_tmp = []
    for num, i in l[::1000].iterrows():
        pivData = pd.read_csv(i.Dir).dropna()
        v = ((pivData.u ** 2 + pivData.v ** 2) ** 0.5 ).mean()
        v_tmp.append(v)
    meanv = np.array(v_tmp).mean()
    meanv_list.append(meanv)
plt.figure(dpi=150)
plt.plot(range(0, 18), np.array(meanv_list)*0.16)
plt.xlabel("sample number")
plt.ylabel("mean velocity (um/s)")
# %% codecell
bf_folder = r"C:\Users\liuzy\Documents\12092021\piv_drop\21"
fl_folder = r"C:\Users\liuzy\Documents\12092021\piv_drop\22"
l1 = readdata(bf_folder, "csv")
data_list1 = []
for num, i in l1[::20].iterrows():
    pivData = pd.read_csv(i.Dir).dropna()
    data_list1.append(pivData)
data_bf = pd.concat(data_list1, axis=0)
data_bf = data_bf.reset_index(drop=True)
data_bf
# %% codecell
l2 = readdata(fl_folder, "csv")
data_list2 = []
for num, i in l2[::20].iterrows():
    pivData = pd.read_csv(i.Dir).dropna()
    data_list2.append(pivData)
data_fl = pd.concat(data_list2, axis=0)
data_fl = data_fl.reset_index(drop=True)
# %% codecell
from myImageLib import bestcolor
plt.figure(dpi=150)
hist, bin_edges = np.histogram(data_bf.u*0.16, bins=np.linspace(-10, 10, 50), density=True)
plt.plot(bin_edges[:-1], hist, ls='solid', color=bestcolor(0), label="bf_u")
hist, bin_edges = np.histogram(data_bf.v*0.16, bins=np.linspace(-10, 10, 50), density=True)
plt.plot(bin_edges[:-1], hist, ls='--', color=bestcolor(0), label="bf_v")
# hist, bin_edges = np.histogram(data_fl.u*0.16, bins=np.linspace(-10, 10, 50), density=True)
# plt.plot(bin_edges[:-1], hist, ls='solid', marker='x', color=bestcolor(0), label="fl_u")
# hist, bin_edges = np.histogram(data_fl.v*0.16, bins=np.linspace(-10, 10, 50), density=True)
# plt.plot(bin_edges[:-1], hist, ls='solid', marker='x', color=bestcolor(1), label="fl_v")
plt.legend()
plt.xlabel("velocity (um/s)")
plt.ylabel("PDF")

# %% codecell
data_bf - data_fl
# %% codecell
pivData
# %% codecell
11100/148
# %% codecell
# oxygen concentration profile in a droplet
K = 5
rs = 0.5
r = np.linspace(0, 1)
C = 1 - 1/6 * K * (1 - r**2)
plt.plot(r, C, label="$K=5$")
K = 10
C = 1 - 1/6 * K * (1 - r**2)
plt.plot(r, C, label="$K=10$")
plt.plot([0, 1], [0, 0], ls="--", color="black")
K = 0.169
C = 1 - 1/6 * K * (1 - r**2)
plt.plot(r, C, label="$K=0.169$", color="red", lw=3)
plt.xlabel("$r/R$")
plt.ylabel("$C/C_0$")
plt.legend()
# %% codecell
8e16 * 10**(-12.7) / 24 / 3600 * (50e-6)**2 / 2.11e-9 / 1.298
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
# %% codecell
