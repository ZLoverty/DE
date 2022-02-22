# This code is for the analysis of spatial and temporal correlations in PIV velocity field
# %% codecell
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from corrLib import readdata, distance_corr, xy_bin, divide_windows
from matplotlib import cm
from pivLib import read_piv
from matplotlib.patches import Ellipse
import scipy
from skimage import io
# %% codecell
# util functions
def autocorr_t(x):
    """Compute the temporal autocorrelation of a 1-D signal.
    Args:
    x -- 1-D signal
    dt -- the time interval between two signals (default to 1)
    Returns:
    corr -- correlation array
    t -- time difference
    """
    xn = x - x.mean()
    corr = np.correlate(xn, xn, mode="same")[len(xn)//2:] / np.inner(xn, xn)
    return corr

def vacf_piv(vstack, dt, mode="direct"):
    """Compute averaged vacf from PIV data.
    This is a wrapper of function autocorr_t(), adding the averaging over all the velocity spots.
    Args:
    vstack -- a 2-D np array of velocity data. axis-0 is time and axes-1,2 are spots in velocity field.
                Usually, this stack can be constracted by `np.stack(u_list)` and then reshape to flatten axes 1 and 2.
    dt -- time between two data points
    mode -- the averaging method, can be "direct" or "weighted".
            "weighted" will use mean velocity as the averaging weight, whereas "direct" uses 1.
    Returns:
    corrData -- DataFrame of (corr, t)
    """
    # rearrange vstack
    assert(len(vstack.shape)==3)
    stack_r = vstack.reshape((vstack.shape[0], -1)).T
    # compute autocorrelation
    corr_list = []
    weight = 1
    normalizer = 0
    for x in stack_r:
        if np.isnan(x[0]) == False: # masked out part has velocity as nan, which cannot be used for correlation computation
            if mode == "weighted":
                weight = abs(x).mean()
            normalizer += weight
            corr = autocorr_t(x) * weight
            corr_list.append(corr)
    corr_mean = np.stack(corr_list, axis=0).sum(axis=0) / normalizer

    return pd.DataFrame({"c": corr_mean, "t": np.arange(len(corr_mean)) * dt}).set_index("t")

def read_piv_stack(folder):
    """Read PIV data in given folder and stack the velocity data"""
    l = readdata(folder, "csv")
    u_list = []
    v_list = []
    for num, i in l.iterrows():
        x, y, u, v = read_piv(i.Dir)
        u_list.append(u)
        v_list.append(v)
    return np.stack(u_list, axis=0), np.stack(v_list, axis=0)
# %% codecell
# test vacf_piv
folder = r"test_files/w10_o5"
l = readdata(folder, "csv")
u_list = []
for num, i in l.iterrows():
    x, y, u, v = read_piv(i.Dir)
    u_list.append(u)
stack = np.stack(u_list, axis=0)
vacf_piv(stack, 0.04, mode="direct").plot()
# %% codecell
fig, ax = plt.subplots(dpi=150)
for n in [19, 10, 20]:
    folder = r"C:\Users\liuzy\Documents\vacf-mask\{:d}\piv_drop".format(n)
    ustack, vstack = read_piv_stack(folder)
    vacf_piv(ustack, 0.04, mode="direct").plot(ax=ax, ls="", marker="o")
ax.set_xlim([0, 1])
# %% codecell
# smooth velocity in time
fig, ax = plt.subplots(dpi=150)
for n in [19, 10, 20]:
    folder = r"C:\Users\liuzy\Documents\vacf-mask\{:d}\piv_drop".format(n)
    ustack, vstack = read_piv_stack(folder)
    ustack = scipy.ndimage.gaussian_filter(ustack, (3/4,0,0))
    vacf_piv(ustack, 0.04, mode="direct").plot(ax=ax, ls="", marker="o")
ax.set_xlim([0, 1])
# %% codecell
stack_r = vstack.reshape((vstack.shape[0], -1)).T
stack1 = stack_r[~np.isnan(stack_r[:, 0]), :]
stack2 = scipy.ndimage.gaussian_filter(stack1, (0, 0.75))
# %% codecell
stack1.shape
# %% codecell
stack_r.shape
# %% codecell
plt.plot(stack1[0])
plt.plot(stack2[0])
# %% codecell
ustack.shape
# %% codecell
# include and exclude edge data
folder = r"C:\Users\liuzy\Documents\vacf-mask\10"
img = io.imread(os.path.join(folder, "images", "00000.tif"))
x, y, u, v = read_piv(os.path.join(folder, "piv_drop", "00000-00001.csv"))
plt.figure(dpi=150)
plt.imshow(img, cmap="gray")
plt.quiver(x, y, u, v, color="yellow", scale=4000, width=0.004)
plt.axis("off")
# %% codecell
mask = io.imread(os.path.join(folder, "mask.tif"))
mask = mask >= mask.mean()
winsize=20
overlap=10
mask_w = divide_windows(mask, windowsize=[winsize, winsize],
                            step=winsize-overlap)[2] >= 1
u1 = u
v1 = v
u1[~mask_w] = np.nan
v1[~mask_w] = np.nan
plt.figure(dpi=150)
plt.imshow(img, cmap="gray")
plt.quiver(x, y, u1, v1, color="yellow", scale=4000, width=0.004)
plt.axis("off")
# %% codecell
# mask -> vacf
fig, ax = plt.subplots(dpi=150)
for n in [19, 10, 20]:
    folder = r"C:\Users\liuzy\Documents\vacf-mask\{:d}\piv_drop".format(n)
    # velocity
    ustack, vstack = read_piv_stack(folder)
    # smooth with gaussian filter
    ustack = scipy.ndimage.gaussian_filter(ustack, (3/4,0,0))
    vacf_piv(ustack, 0.04, mode="direct").plot(ax=ax, ls="", marker="o")
    # mask
    mask = io.imread(os.path.join(folder, "..\mask.tif"))
    mask = mask >= mask.mean()
    winsize=20
    overlap=10
    mask_w = divide_windows(mask, windowsize=[winsize, winsize],
                                step=winsize-overlap)[2] >= 1
    mask_wb = np.broadcast_to(mask_w, ustack.shape)
    # apply mask
    ustack[~mask_wb] = np.nan
    vacf_piv(ustack, 0.04, mode="direct").plot(ax=ax, ls="", marker="o")
    break
ax.set_xlim([0, 1])
# %% codecell
folder = r"C:\Users\liuzy\Documents\vacf-mask\{:d}\piv_drop".format(10)
ustack, vstack = read_piv_stack(folder)
# %% codecell
# construct droplet position data
abr = {"19": (172, 164, 168),
       "10": (395, 377, 508),
       "20": (526, 514, 704)}
# %% codecell
# systematic vary radial position

dr = 3 # um
mpp = 0.16 # micron per pixel
for n in [19, 10, 20]:
    fig, ax = plt.subplots(dpi=150)
    folder = r"C:\Users\liuzy\Documents\vacf-mask\{:d}\piv_drop".format(n)
    x, y, u, v = read_piv(os.path.join(folder, "00000-00001.csv"))
    # velocity
    ustack, vstack = read_piv_stack(folder)
    # smooth with gaussian filter
    ustack = scipy.ndimage.gaussian_filter(ustack, (3/4,0,0))
    vacf_piv(ustack, 0.04, mode="direct").plot(ax=ax, marker="o")
    # mask
    a, b, r = abr[str(n)]
    N_bins = np.floor(r / dr * mpp)
    r_stops = np.linspace(0, r, int(N_bins))
    for r_stop in r_stops[1:]:
        mask_w = (x - a) ** 2 + (y - b) ** 2 <= r_stop ** 2
        plt.figure()
        mask_wb = np.broadcast_to(mask_w, ustack.shape)
        # apply mask
        c = np.copy(ustack)
        c[~mask_wb] = np.nan
        plt.imshow(c[0])
        vacf_piv(c, 0.04, mode="direct").plot(ax=ax)
    ax.set_xlim([0, 1])
    break
# %% codecell
# mask and mean velocity, time evolution
abr = {"19": (172, 164, 168/2),
       "10": (395, 377, 508/2),
       "20": (526, 514, 704/2)}

mpp = 0.16 # micron per pixel

for n in [19, 10, 20]:
    fig, ax = plt.subplots(dpi=150)
    folder = r"C:\Users\liuzy\Documents\vacf-mask\{:d}\piv_drop".format(n)
    x, y, u, v = read_piv(os.path.join(folder, "00000-00001.csv"))
    # velocity
    ustack, vstack = read_piv_stack(folder)
    # smooth with gaussian filter
    ustack = scipy.ndimage.gaussian_filter(ustack, (3/4,0,0))
    # mask
    a, b, r = abr[str(n)]
    dr =  r / 8 * mpp
    N_bins = np.floor(r / dr * mpp)
    r_stops = np.linspace(0, r, int(N_bins))
    for r_stop in r_stops[1:]:
        mask_w = (x - a) ** 2 + (y - b) ** 2 <= r_stop ** 2
        mask_wb = np.broadcast_to(mask_w, ustack.shape)
        # apply mask
        u1 = np.copy(ustack)
        v1 = np.copy(vstack)
        u1[~mask_wb] = np.nan
        v1[~mask_wb] = np.nan
        velocity = (u1 ** 2 + v1 ** 2) ** 0.5
        ax.plot(np.nanmean(velocity, axis=(1, 2))*0.16,
            label="$r_{{stop}}={:.2f}r$".format(r_stop/r))
    ax.legend(bbox_to_anchor=(1,1))
    ax.set_xlabel("time (frame)")
    ax.set_ylabel("mean velocity (um/s)")
    ax.set_xlim([0, 250])
    ax.set_ylim([0, 30])


# %% codecell
# mask and mean velocity, vmean vs. r_stop
abr = {"19": (172, 164, 168/2),
       "10": (395, 377, 508/2),
       "20": (526, 514, 704/2)}

mpp = 0.16 # micron per pixel

fig, ax = plt.subplots(dpi=150)
for n in [19, 10, 20]:
    folder = r"C:\Users\liuzy\Documents\vacf-mask\{:d}\piv_drop".format(n)
    x, y, u, v = read_piv(os.path.join(folder, "00000-00001.csv"))
    # velocity
    ustack, vstack = read_piv_stack(folder)
    # smooth with gaussian filter
    ustack = scipy.ndimage.gaussian_filter(ustack, (3/4,0,0))
    # mask
    a, b, r = abr[str(n)]
    dr =  r / 8 * mpp
    N_bins = np.floor(r / dr * mpp)
    r_stops = np.linspace(0, r, int(N_bins))
    v_list = []
    for r_stop in r_stops[1:]:
        mask_w = (x - a) ** 2 + (y - b) ** 2 <= r_stop ** 2
        mask_wb = np.broadcast_to(mask_w, ustack.shape)
        # apply mask
        u1 = np.copy(ustack)
        v1 = np.copy(vstack)
        u1[~mask_wb] = np.nan
        v1[~mask_wb] = np.nan
        velocity = (u1 ** 2 + v1 ** 2) ** 0.5
        v_list.append(np.nanmean(velocity) * mpp)
    plt.plot(r_stops[1:], v_list, label="{:.1f}".format(r*2*mpp))
ax.legend(bbox_to_anchor=(1,1))
ax.set_xlabel("$r_{{stop}}/r$")
ax.set_ylabel("mean velocity (um/s)")

# %% codecell
# only exclude edge data - mean velocity
folder = r"C:\Users\liuzy\Documents\vacf-mask\{:d}\piv_drop".format(n)
x, y, u, v = read_piv(os.path.join(folder, "00000-00001.csv"))
ustack, vstack = read_piv_stack(folder)
ustack = scipy.ndimage.gaussian_filter(ustack, (3/4,0,0))
vstack = scipy.ndimage.gaussian_filter(vstack, (3/4,0,0))
vmean = (ustack ** 2 + vstack ** 2) ** 0.5
vmean_t = np.nanmean(vmean, axis=(1, 2)) * mpp
plt.plot(vmean_t)
mask = io.imread(os.path.join(folder, "..\mask.tif"))
mask = mask > mask.mean()
mask_w = divide_windows(mask, windowsize=[winsize, winsize],
                            step=winsize-overlap)[2] >= 1
mask_wb = np.broadcast_to(mask_w, ustack.shape)
u1 = np.copy(ustack)
v1 = np.copy(vstack)
u1[~mask_wb] = np.nan
v1[~mask_wb] = np.nan
vmean_ee = (u1 ** 2 + v1 ** 2) ** 0.5
vmean_ee_t = np.nanmean(vmean_ee, axis=(1, 2)) * mpp
plt.plot(vmean_ee_t)
plt.xlabel("time (frame)")
plt.ylabel("mean velocity (um/s)")
# %% codecell
l = readdata(r"..\Notes", "pdf")
for num, i in l.iterrows():
    print(i.Name)
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
