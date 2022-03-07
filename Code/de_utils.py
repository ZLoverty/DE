import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter
from pivLib import read_piv
from skimage import io
from corrLib import divide_windows, readdata
import trackpy as tp
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

# %% codecell
class de_data():
    """
    Double emulsion data plotting tool.
    """
    def __init__(self, data):
        self.data = data
    def __repr__(self):
        return(str(self.data))
    def show(self):
        print(self.data)
    def parameter_space(self, highlight_Chile_data=True):
        """D vs. d, with color coded OD"""
        log1 = self.data.dropna(subset=["Rinfy", "t2"])
        binsize = 20 # OD bin size
        plt.figure(figsize=(3.5,3),dpi=100)
        bin_starts = range(0, int(log1.OD.max()), binsize)
        cmap = plt.cm.get_cmap("tab10")
        for num, bs in enumerate(bin_starts):
            log2 = log1.loc[(log1.OD>bs)&(log1.OD<=bs+binsize)]
            if highlight_Chile_data == True:
                log3 = log2.loc[log2.Comment!="Chile"]
                log4 = log2.loc[log2.Comment=="Chile"]
                plt.scatter(log3.D, log3.d, color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
                plt.scatter(log4.D, log4.d, edgecolors=cmap(num), marker="^", fc=(0,0,0,0))
            else:
                plt.scatter(log2.D, log2.d, color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
        plt.xlabel("$D$ (um)")
        plt.ylabel("$d$ (um)")
        plt.xlim([0, 1.05*log1.D.max()])
        plt.ylim([0, 1.05*log1.d.max()])
        plt.plot([0, 1.05*log1.d.max()], [0, 1.05*log1.d.max()], ls=":", color="black")
        plt.legend(ncol=2, fontsize=5, loc="upper left")
    def generate_msd_repo(self, component="y", data_dir=r"..\Data\traj"):
        """Generate .jpg images for MSD repo. Takes ~2 min and save images, be careful!
        coord: the displacement component to compute, can be 'y' or 'z'.
        Edit:
        Mar 03, 2022 -- i) add z component, ii) put all DE# in image file name"""
        mapper = {"y": "<y^2>", "z": "<x^2>"}
        log1 = self.data.dropna(subset=["OD"])
        if component == "z":
            log1 = log1.loc[log1.Plane=="XZ"]
        elif component == "y":
            pass
        else:
            raise ValueError("Invalid component, should be y or z")
        viridis = plt.cm.get_cmap('Set1', 5)
        count = 0
        plt.figure(dpi=150)
        name_list = []
        for num, i in log1.iterrows():
            traj_dir = os.path.join(data_dir, "{:02d}.csv".format(int(i["DE#"])))
            if os.path.exists(traj_dir):
                traj = pd.read_csv(traj_dir)
            else:
                print("Missing traj {:d}".format(i["DE#"]))
                continue
            msd = tp.msd(traj, mpp=1, fps=i.FPS, max_lagtime=traj.frame.max()//5).dropna()
            plt.plot(msd.lagt, msd[mapper[component]], label=i["DE#"], color=viridis(count/4))
            count += 1
            name_list.append("{:d}".format(int(i["DE#"])))
            if count > 4:
                plt.legend(fontsize=20, frameon=False)
                plt.xlabel("$\Delta t$ (s)")
                if component == "y":
                    plt.ylabel(r"$\left< \Delta y^2 \right>$ ($\mu$m$^2$)")
                elif component == "z":
                    plt.ylabel(r"$\left< \Delta z^2 \right>$ ($\mu$m$^2$)")
                plt.grid(which="both", ls=":")
                plt.loglog()
                plt.savefig("{}.jpg".format("-".join(name_list)))
                plt.figure(dpi=150)
                count = 0
                name_list = []
        plt.legend(fontsize=20, frameon=False)
        plt.xlabel("$\Delta t$ (s)")
        if component == "y":
            plt.ylabel(r"$\left< \Delta y^2 \right>$ ($\mu$m$^2$)")
        elif component == "z":
            plt.ylabel(r"$\left< \Delta z^2 \right>$ ($\mu$m$^2$)")
        plt.grid(which="both", ls=":")
        plt.loglog()
        plt.tight_layout()
        plt.savefig("{:d}.jpg".format(num))
    def scatter_0(self, mode="log", highlight_Chile_data=True):
        """Plot tau^* vs. (D-d)/d^2"""
        log1 = self.data.dropna(subset=["Rinfy", "t2"])
        binsize = 20 # OD bin size
        plt.figure(figsize=(3.5,3), dpi=100)
        bin_starts = range(0, int(log1.OD.max()), binsize)
        cmap = plt.cm.get_cmap("tab10")
        for num, bs in enumerate(bin_starts):
            log2 = log1.loc[(log1.OD>bs)&(log1.OD<=bs+binsize)]
            if highlight_Chile_data == True:
                log3 = log2.loc[log2.Comment!="Chile"]
                log4 = log2.loc[log2.Comment=="Chile"]
                plt.scatter(log3["(D-d)/d^2"], log3.t2, color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
                plt.scatter(log4["(D-d)/d^2"], log4.t2, edgecolors=cmap(num), marker="^", fc=(0,0,0,0))
            else:
                plt.scatter(log2["(D-d)/d^2"], log2.t2, color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
        plt.xlabel("$(D-d)/d^2$")
        plt.ylabel("$\\tau^*$ (s)")
        plt.legend(ncol=2, fontsize=6)
        plt.grid(which="both", ls=":")
        if mode == "log":
            plt.loglog()
    def look_for_missing_traj(self, traj_folder, fmt="{:02d}.csv"):
        """Check the existence of trajectory data file in given folder, according to the log"""
        log1 = self.data.dropna(subset=["OD"])
        n_missing = 0
        for num, i in log1.iterrows():
            traj_dir = os.path.join(traj_folder, fmt.format(int(i["DE#"])))
            if os.path.exists(traj_dir):
                traj = pd.read_csv(traj_dir)
            else:
                print("Missing traj {:d}".format(i["DE#"]))
                n_missing += 1
        print("{:d} trajectories are missing".format(n_missing))
    def plot_MSD_model_Cristian(self):
        """plot the MSD model, get a feeling of parameters, save for future use, not finished"""
        gamma = 2
        nu = 1
        t = np.logspace(-2, 2)
        y2 = (1 - np.exp(-2*gamma*t)) / (2*gamma) - (np.exp(-(gamma+nu)*t)-np.exp(-2*gamma*t))
        gamma = 0.5
        y3 = (1 - np.exp(-2*gamma*t)) / (2*gamma) - (np.exp(-(gamma+nu)*t)-np.exp(-2*gamma*t))
        plt.figure(figsize=(3.5, 3), dpi=100)
        plt.plot(t, y2, label="$\\tau=1, \\tau^*=0.5$")
        plt.plot(t, y3, label="$\\tau=1, \\tau^*=2$")
        plt.legend()
        plt.loglog()
        plt.grid(which="both", ls=":")
        plt.xlabel("lag time")
        plt.ylabel("$\left<\Delta y^2\\right>$")
    def plot_0(self, nbins=5, overlap=0, mode="log"):
        """tau vs. (D-d)/d^2, with average"""
        log = self.data
        xm = 0
        ym = 0
        cmap = plt.cm.get_cmap("tab10")
        plt.figure(figsize=(3.5,3), dpi=100)
        for num, OD_min in enumerate(range(0, 160, 20)):
            OD_max = OD_min + 20
            log1 = log.loc[(log.OD>=OD_min)&(log.OD<=OD_max)].dropna(subset=["Rinfy"])
            r = (log1.D - log1.d) / log1.d ** 2
            # visualize the bins
            # plt.figure(dpi=100)
            # plt.scatter(r, log1["DE#"])
            # for num, i in log1.iterrows():
            #     plt.annotate(i["DE#"], ((i.D - i.d) / i.d ** 2, i["DE#"]), xycoords="data")
            # plt.xlabel("$(D-d)/d^2$")
            # plt.ylabel("DE index")
            if mode == "log":
                bins = np.logspace(np.log(r.min()), np.log(r.max()), nbins+1)
            else:
                bins = np.linspace(r.min(), r.max(), nbins+1)
            bin_start = bins[:-1]
            bin_size = bins[1:] - bins[:-1]
            bin_end = bin_start + bin_size * (1 + overlap)
            # count = 20
            # for start, end in zip(bin_start, bin_end):
            #     plt.plot([start, end], [count, count])
            #     count += 2
            # plot Rinf as a function of B
            count = 0
            for start, end in zip(bin_start, bin_end):
                log2 = log1.loc[(r>=start)&(r<=end)]
                r2 = (log2.D - log2.d) / log2.d ** 2
                x = r2.mean()
                y =(log2.t2).mean()
                xe = r2.std()
                ye = (log2.t2).std()
                if count == 0:
                    plt.errorbar(x, y, xerr=xe, yerr=ye, marker="o", color=cmap(num), label="{0:d}-{1:d}".format(OD_min, OD_max))
                    count += 1
                else:
                    plt.errorbar(x, y, xerr=xe, yerr=ye, marker="o", color=cmap(num))
                if np.isnan(xe):
                    xe = 0
                if np.isnan(ye):
                    ye = 0
                if x + xe > xm:
                    xm = x + xe
                if y + ye > ym:
                    ym = y + ye
        plt.xlabel("$(D-d)/d^2$")
        plt.ylabel("$\\tau^*$ (s)")
        plt.legend(ncol=2, fontsize=6, loc="lower right")
        if mode == "log":
            plt.loglog()
            plt.grid(which="both", ls=":")
        else:
            plt.xlim([0, xm*1.1])
            plt.ylim([0, ym*1.1])
    def scatter_1(self, mode="log", highlight_Chile_data=True):
        """R_inf vs. (D-d)/d^2"""
        log1 = self.data.dropna(subset=["Rinfy", "t2"])
        binsize = 20 # OD bin size
        plt.figure(figsize=(3.5,3), dpi=100)
        bin_starts = range(0, int(log1.OD.max()), binsize)
        cmap = plt.cm.get_cmap("tab10")
        for num, bs in enumerate(bin_starts):
            log2 = log1.loc[(log1.OD>bs)&(log1.OD<=bs+binsize)]
            if highlight_Chile_data == True:
                log3 = log2.loc[log2.Comment!="Chile"]
                log4 = log2.loc[log2.Comment=="Chile"]
                plt.scatter(log3["(D-d)/d^2"], log3.Rinfy**0.5, color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
                plt.scatter(log4["(D-d)/d^2"], log4.Rinfy**0.5, edgecolors=cmap(num), marker="^", fc=(0,0,0,0))
            else:
                plt.scatter(log2["(D-d)/d^2"], log2.Rinfy**0.5, color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
        plt.xlabel("$(D-d)/d^2$")
        plt.ylabel("$R_\infty$ (um)")
        plt.legend(ncol=2, fontsize=6)
        plt.grid(which="both", ls=":")
        if mode == "log":
            plt.loglog()
    def plot_1(self, nbins=5, overlap=0, mode="log"):
        """R_inf vs. (D-d)/d^2, with average"""
        log = self.data
        xm = 0
        ym = 0
        cmap = plt.cm.get_cmap("tab10")
        plt.figure(figsize=(3.5,3), dpi=100)
        for num, OD_min in enumerate(range(0, 160, 20)):
            OD_max = OD_min + 20
            log1 = log.loc[(log.OD>=OD_min)&(log.OD<=OD_max)].dropna(subset=["Rinfy"])
            r = (log1.D - log1.d) / log1.d ** 2
            # visualize the bins
            # plt.figure(dpi=100)
            # plt.scatter(r, log1["DE#"])
            # for num, i in log1.iterrows():
            #     plt.annotate(i["DE#"], ((i.D - i.d) / i.d ** 2, i["DE#"]), xycoords="data")
            # plt.xlabel("$(D-d)/d^2$")
            # plt.ylabel("DE index")
            if mode == "log":
                bins = np.logspace(np.log(r.min()), np.log(r.max()), nbins+1)
            else:
                bins = np.linspace(r.min(), r.max(), nbins+1)
            bin_start = bins[:-1]
            bin_size = bins[1:] - bins[:-1]
            bin_end = bin_start + bin_size * (1 + overlap)
            # count = 20
            # for start, end in zip(bin_start, bin_end):
            #     plt.plot([start, end], [count, count])
            #     count += 2
            # plot Rinf as a function of B
            count = 0
            for start, end in zip(bin_start, bin_end):
                log2 = log1.loc[(r>=start)&(r<=end)]
                r2 = (log2.D - log2.d) / log2.d ** 2
                x = r2.mean()
                y =(log2.Rinfy**0.5).mean()
                xe = r2.std()
                ye = (log2.Rinfy**0.5).std()
                if count == 0:
                    plt.errorbar(x, y, xerr=xe, yerr=ye, marker="o", color=cmap(num), label="{0:d}-{1:d}".format(OD_min, OD_max))
                    count += 1
                else:
                    plt.errorbar(x, y, xerr=xe, yerr=ye, marker="o", color=cmap(num))
                if np.isnan(xe):
                    xe = 0
                if np.isnan(ye):
                    ye = 0
                if x + xe > xm:
                    xm = x + xe
                if y + ye > ym:
                    ym = y + ye
        plt.xlabel("$(D-d)/d^2$")
        plt.ylabel("$R_\infty$ (um)")
        plt.legend(ncol=2, fontsize=6, loc="lower right")
        if mode == "log":
            plt.loglog()
            plt.grid(which="both", ls=":")
        else:
            plt.xlim([0, xm*1.1])
            plt.ylim([0, ym*1.1])
    def Rinf2_tau(self):
        """Plot $R_\infty^2$ vs. $\tau^*$"""
        log = self.data
        log1 = log.dropna(subset=["Rinfy", "t2"])
        binsize = 20 # OD bin size
        plt.figure(figsize=(3.5,3), dpi=100)
        bin_starts = range(0, int(log1.OD.max()), binsize)
        cmap = plt.cm.get_cmap("tab10")
        for num, bs in enumerate(bin_starts):
            log2 = log1.loc[(log1.OD>bs)&(log1.OD<=bs+binsize)]
            log3 = log2.loc[log2.Comment!="Chile"]
            log4 = log2.loc[log2.Comment=="Chile"]
            plt.scatter(log3.t2, log3.Rinfy, color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
            plt.scatter(log4.t2, log4.Rinfy, edgecolors=cmap(num), marker="^", fc=(0,0,0,0))
        plt.xlabel("$\\tau^*$ (s)")
        plt.ylabel("$R_\infty^2 $ (um$^2$)")
        plt.legend(ncol=2, fontsize=6, loc="lower right")
        plt.grid(which="both", ls=":")
        plt.xlim([1, 30])
        plt.loglog()
    def Rinf2_over_tau(self):
        """Plot $R_\infty^2 / \tau^*$ vs. $(D-d)/d^2$"""
        log = self.data
        log1 = log.dropna(subset=["Rinfy", "t2"])
        binsize = 20 # OD bin size
        plt.figure(figsize=(3.5,3), dpi=100)
        bin_starts = range(0, int(log1.OD.max()), binsize)
        cmap = plt.cm.get_cmap("tab10")
        for num, bs in enumerate(bin_starts):
            log2 = log1.loc[(log1.OD>bs)&(log1.OD<=bs+binsize)]
            log3 = log2.loc[log2.Comment!="Chile"]
            log4 = log2.loc[log2.Comment=="Chile"]
            plt.scatter(log3["(D-d)/d^2"], log3.Rinfy/(log3.t2), color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
            plt.scatter(log4["(D-d)/d^2"], log4.Rinfy/(log4.t2), edgecolors=cmap(num), marker="^", fc=(0,0,0,0))

        plt.xlabel("$(D-d)/d^2$")
        plt.ylabel("$R_\infty^2 / \\tau^*$")
        plt.legend(ncol=2, fontsize=6, loc="lower right")
        plt.grid(which="both", ls=":")
        plt.loglog()
    def rescale_Rinf_OD(self):
        """Plot Rinf/OD vs. (D-d)/d^2"""
        log = self.data
        log1 = log.dropna(subset=["Rinfy", "t2"])
        binsize = 20 # OD bin size
        plt.figure(figsize=(3.5,3), dpi=100)
        bin_starts = range(0, int(log1.OD.max()), binsize)
        cmap = plt.cm.get_cmap("tab10")
        for num, bs in enumerate(bin_starts):
            log2 = log1.loc[(log1.OD>bs)&(log1.OD<=bs+binsize)]
            log3 = log2.loc[log2.Comment!="Chile"]
            log4 = log2.loc[log2.Comment=="Chile"]
            plt.scatter(log3["(D-d)/d^2"], log3.Rinfy**0.5/(log3.OD), color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
            plt.scatter(log4["(D-d)/d^2"], log4.Rinfy**0.5/(log4.OD), edgecolors=cmap(num), marker="^", fc=(0,0,0,0))
        plt.xlabel("$(D-d)/d^2$")
        plt.ylabel("$R_\infty / OD$")
        plt.legend(ncol=2, fontsize=6)
        plt.grid(which="both", ls=":")
        plt.loglog()
    def rescale_Rinf_freespace(self):
        # rescale Rinf with (D-d)
        log = self.data
        log1 = log.dropna(subset=["Rinfy", "t2"])
        binsize = 20 # OD bin size
        plt.figure(figsize=(3.5, 3), dpi=100)
        bin_starts = range(0, int(log1.OD.max()), binsize)
        cmap = plt.cm.get_cmap("tab10")
        for num, bs in enumerate(bin_starts):
            log2 = log1.loc[(log1.OD>bs)&(log1.OD<=bs+binsize)]
            log3 = log2.loc[log2.Comment!="Chile"]
            log4 = log2.loc[log2.Comment=="Chile"]
            plt.scatter(log3["(D-d)/d^2"], log3.Rinfy**0.5/(log3.D-log3.d), color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
            plt.scatter(log4["(D-d)/d^2"], log4.Rinfy**0.5/(log4.D-log4.d), edgecolors=cmap(num), marker="^", fc=(0,0,0,0))
        plt.xlabel("$(D-d)/d^2$")
        plt.ylabel("$R_\infty / (D-d)$")
        plt.legend(ncol=2, fontsize=6)
        plt.grid(which="both", ls=":")
        plt.loglog()
    def scatter(self, mode="log", highlight_Chile_data=True):
        """I want to implement a more flexible plotting tool to test ideas, but it seems difficult"""
        pass
# %% codecell
class drop_data:
    """Droplet data plotting tool."""
    def __init__(self, data):
        """Initialize a data object with main log spreadsheet (pd.DataFrame)"""
        self.data = data
        self.OD_to_nc = 8e8 # OD to number concentration conversion factor, cells/ml
        self.single_bacterial_volume = 1 # um^3
    def __repr__(self):
        return self.data.__repr__()
    def parameter_space(self):
        """Plot the parameter space of current data, D vs. OD"""
        fig, ax = plt.subplots(figsize=(3.5, 3), dpi=100)
        ax.scatter(self.data["Bacterial concentration"], self.data["Droplet size"])
        ax.set_xlabel("OD")
        ax.set_ylabel("$D$ (um)")
    def find_lifetime_data(self, n=5):
        """Return the Droplet#'s of droplets with more than n videos, n is 5 by default"""
        self.lifetime_data_list = []
        for i in self.data["Droplet#"].drop_duplicates():
            subdata = self.data.loc[self.data["Droplet#"]==i]
            if len(subdata) >= n:
                self.lifetime_data_list.append(i)
        # print("Lifetime data located: {}".format(str(self.lifetime_data_list)))
    def plot_mean_velocity_evolution(self, n=5, mode="log"):
        """Plot mean velocity vs. time.
        Use the time of first video as 0 (or 1 in log mode)
        n: number of curves on each plot
        mode: the scale of time axis, can be 'lin' or 'log' (default)"""
        self.find_lifetime_data()
        cmap = plt.cm.get_cmap("Set1")
        for num, i in enumerate(self.lifetime_data_list):
            if num % n == 0:
                fig, ax = plt.subplots(figsize=(3.5, 2), dpi=100)
                ax.set_xlabel("time (min)")
                ax.set_ylabel("mean velocity (um/s)")
                ax.set_xlim([0, 60])
                if mode == "log":
                    ax.set_xlim([1, 60])
                    ax.set_xscale("log")
                ax.set_ylim([0, 15])
            subdata = self.data.loc[self.data["Droplet#"]==i]
            t = subdata["Time in minutes"]
            t -= subdata["Time in minutes"].min()
            v = subdata["Initial mean velocity (10 s)"]
            if mode == "log":
                t += 1
            ax.plot(t, v, marker="s", color=cmap(num % n), label="{:d}".format(i))
            ax.legend(frameon=False)
    def plot_droplet_size_evolution(self, n=5, mode="log"):
        """Plot droplet size vs. time.
        Use the time of first video as 0 (or 1 in log mode)
        n: number of curves on each plot
        mode: the scale of time axis, can be 'lin' or 'log' (default)"""
        self.find_lifetime_data()
        cmap = plt.cm.get_cmap("Set1")
        for num, i in enumerate(self.lifetime_data_list):
            if num % n == 0:
                fig, ax = plt.subplots(figsize=(3.5, 2), dpi=100)
                ax.set_xlabel("time (min)")
                ax.set_ylabel("droplet diameter (um)")
                ax.set_xlim([0, 60])
                if mode == "log":
                    ax.set_xlim([1, 60])
                    ax.set_xscale("log")
                if mode == "loglog":
                    ax.set_xlim([1, 60])
                    ax.set_xscale("log")
                    ax.set_yscale("log")
                # ax.set_ylim([0, 15])
            subdata = self.data.loc[self.data["Droplet#"]==i]
            t = subdata["Time in minutes"]
            t -= subdata["Time in minutes"].min()
            D = subdata["Droplet size"]
            if mode == "log":
                t += 1
            ax.plot(t, D, marker="s", color=cmap(num % n), label="{:d}".format(i))
            ax.legend(frameon=False)
    def plot_volume_fraction_evolution(self, n=5, mode="log"):
        """Plot droplet size vs. time.
        Use the time of first video as 0 (or 1 in log mode)
        n: number of curves on each plot
        mode: the scale of time axis, can be 'lin' or 'log' (default)"""
        self.find_lifetime_data()
        cmap = plt.cm.get_cmap("Set1")

        for num, i in enumerate(self.lifetime_data_list):
            if num % n == 0:
                fig, ax = plt.subplots(figsize=(3.5, 2), dpi=100)
                ax.set_xlabel("time (min)")
                ax.set_ylabel("volume fraction")
                ax.set_xlim([0, 60])
                if mode == "log":
                    ax.set_xlim([1, 60])
                    ax.set_xscale("log")
                ax.set_ylim([0.1, 0.3])
            subdata = self.data.loc[self.data["Droplet#"]==i]
            initial_droplet_volume = 4/3 * np.pi * (subdata["Droplet size"].iloc[0]/2) ** 3
            bacterial_volume = subdata["Bacterial concentration"].iloc[0] * self.OD_to_nc * initial_droplet_volume * 1e-12 * self.single_bacterial_volume

            t = subdata["Time in minutes"]
            t -= subdata["Time in minutes"].min()
            vf = bacterial_volume / (4/3 * np.pi * (subdata["Droplet size"]/2) ** 3)
            if mode == "log":
                t += 1
            ax.plot(t, vf, marker="s", color=cmap(num % n), label="{:d}".format(i))
            ax.legend(frameon=False)
    def plot_velocity_volume_fraction_correlation(self, time_bins=5):
        """Plot the correlation between mean velocity and volume fraction
        time_bins: number of time bins"""
        self.find_lifetime_data()
        cmap = plt.cm.get_cmap("Set1")
        bin_size = 60 // time_bins
        bin_starts = range(0, 60, bin_size)
        plot_data_list = []
        for num, i in enumerate(self.lifetime_data_list):
            subdata = self.data.loc[self.data["Droplet#"]==i]
            initial_droplet_volume = 4/3 * np.pi * (subdata["Droplet size"].iloc[0]/2) ** 3
            bacterial_volume = subdata["Bacterial concentration"].iloc[0] * self.OD_to_nc * initial_droplet_volume * 1e-12 * self.single_bacterial_volume
            t = subdata["Time in minutes"]
            t -= subdata["Time in minutes"].min()
            vf = bacterial_volume / (4/3 * np.pi * (subdata["Droplet size"]/2) ** 3)
            plot_data = subdata.assign(t=t, vf=vf)
            plot_data_list.append(plot_data)
        data = pd.concat(plot_data_list, axis=0)
        fig, ax = plt.subplots(figsize=(3.5, 3), dpi=100)
        for num, start in enumerate(bin_starts):
            subdata = data.loc[(data.t>start)&(data.t<=start+bin_size)]
            ax.scatter(subdata.vf, subdata["Initial mean velocity (10 s)"],
                       color=cmap(num), label="{0:.0f}-{1:.0f}".format(start, start+bin_size))
        ax.set_xlabel("volume fraction")
        ax.set_ylabel("mean velocity")
        ax.legend()
# %% codecell


# %% codecell
if __name__=="__main__":
    # test de_data class
    # %% codecell
    # make all the plots
    log_dir = r"..\Data\structured_log_DE.ods"
    log = pd.read_excel(io=log_dir, sheet_name="main")
    data = de_data(log)
    data.parameter_space(highlight_Chile_data=True) # 1
    data.plot_MSD_model_Cristian() # 3
    data.scatter_0(mode="log", highlight_Chile_data=True) # 2
    data.plot_0(nbins=5, overlap=0, mode="log") # 4
    data.scatter_1(mode="log", highlight_Chile_data=True) # 5
    data.plot_1(nbins=5, overlap=0, mode="log") # 6
    data.Rinf2_tau() # 7
    data.Rinf2_over_tau() # 8
    data.rescale_Rinf_OD() # 9
    data.rescale_Rinf_freespace() # 10
    # %% codecell
    # generate_msd_repo method generates .jpg images, and take longer time to run
    # (several minutes), use caution when running this block
    data.generate_msd_repo(component="z")



    # %% codecell
    # test drop_data class
    # create drop_data object
    log_dir = r"..\Data\structured_log.ods"
    log = pd.read_excel(io=log_dir, sheet_name="main")
    dd = drop_data(log)
    # %% codecell
    dd.parameter_space()
    # %% codecell
    # test find_lifetime_data()
    dd.find_lifetime_data()
    # %% codecell
    dd.plot_mean_velocity_evolution(n=6, mode="log")
    # %% codecell
    dd.plot_droplet_size_evolution(n=6, mode="log")
    # %% codecell
    dd.plot_volume_fraction_evolution(n=6, mode="lin")
    # %% codecell
    dd.plot_velocity_volume_fraction_correlation(time_bins=6)
