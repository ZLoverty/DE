# %% codecell
from openpiv import tools, pyprocess, validation, filters, scaling
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import os
from scipy.signal import medfilt2d
import pandas as pd
from corrLib import divide_windows
import time
# %% codecell
def PIV(I0, I1, winsize, overlap, dt):
    """ Normal PIV """
    u0, v0, sig2noise = pyprocess.extended_search_area_piv(
        I0.astype(np.int32),
        I1.astype(np.int32),
        window_size=winsize,
        overlap=overlap,
        dt=dt,
        search_area_size=winsize,
        sig2noise_method='peak2peak',
    )
    # get x, y
    x, y = pyprocess.get_coordinates(
        image_size=I0.shape,
        search_area_size=winsize,
        overlap=overlap,
        window_size=winsize
    )
    u1, v1, mask_s2n = validation.sig2noise_val(
        u0, v0,
        sig2noise,
        threshold = 1.05,
    )
    # replace_outliers
    u2, v2 = filters.replace_outliers(
        u1, v1,
        method='localmean',
        max_iter=3,
        kernel_size=3,
    )
    # median filter smoothing
    u3 = medfilt2d(u2, 3)
    v3 = medfilt2d(v2, 3)
    return x, y, u3, v3
# %% codecell
def PIV_masked_1(I0, I1, winsize, overlap, dt, mask):
    """Test different masking procedures.
    1. Mask raw images by setting background 0, then apply PIV.
    2. Mask raw images by setting background nan, then apply PIV.
    3. Apply PIV directly on raw images, then apply mask on velocity.
    """
    assert(mask.shape==I0.shape)
    mask = mask >= mask.mean() # convert mask to boolean array
    I0 = I0 * mask
    I1 = I1 * mask
    x, y, u, v = PIV(I0, I1, winsize, overlap, dt)
    mask_w = divide_windows(mask, windowsize=[winsize, winsize], step=winsize-overlap)[2] >= 1
    assert(mask_w.shape==x.shape)
    u[~mask_w] = np.nan
    v[~mask_w] = np.nan
    return x, y, u, v
# %% codecell
def PIV_masked_2(I0, I1, winsize, overlap, dt, mask):
    """Test different masking procedures.
    1. Mask raw images by setting background 0, then apply PIV.
    2. Mask raw images by setting background nan, then apply PIV.
    3. Apply PIV directly on raw images, then apply mask on velocity.
    """
    assert(mask.shape==I0.shape)
    mask = mask >= mask.mean() # convert mask to boolean array
    x, y, u, v = PIV(I0, I1, winsize, overlap, dt)
    mask_w = divide_windows(mask, windowsize=[winsize, winsize], step=winsize-overlap)[2] >= 1
    assert(mask_w.shape==x.shape)
    u[~mask_w] = np.nan
    v[~mask_w] = np.nan
    return x, y, u, v
# %% codecell
def PIV_masked_3(I0, I1, winsize, overlap, dt, mask):
    """Test different masking procedures.
    1. Mask raw images by setting background 0, then apply PIV.
    2. Mask raw images by setting background nan, then apply PIV.
    3. Apply PIV directly on raw images, then apply mask on velocity.
    """
    assert(mask.shape==I0.shape)
    mask = mask >= mask.mean() # convert mask to boolean array
    I0[~mask] = np.nan
    I1[~mask] = np.nan
    x, y, u, v = PIV(I0, I1, winsize, overlap, dt)
    mask_w = divide_windows(mask, windowsize=[winsize, winsize], step=winsize-overlap)[2] >= 1
    assert(mask_w.shape==x.shape)
    u[~mask_w] = np.nan
    v[~mask_w] = np.nan
    return x, y, u, v
# %% codecelle
I0 = io.imread(os.path.join("img", "I10.tif"))
I1 = io.imread(os.path.join("img", "I11.tif"))
mask = io.imread(os.path.join("img", "mask1.tif"))
winsize = 40
overlap = 20
dt = 0.02
x, y, u, v = [], [], [], []
for func in [PIV_masked_1, PIV_masked_2]:
    x1, y1, u1, v1 = func(I0, I1, winsize, overlap, dt, mask)
    x.append(x1); y.append(y1); u.append(u1); v.append(v1)
fig, ax = plt.subplots(nrows=1, ncols=2, dpi=200)
for i in [0, 1]:
    ax[i].imshow(I0, cmap='gray')
    ax[i].quiver(x[i], y[i], u[i], v[i], color='yellow')
    ax[i].axis('off')
fig.savefig(os.path.join("img", "compare_piv.jpg"))
# %% codecell
print("The two masking procedures don't produce very different results, according to visual inspection.")
print("I also plot the velocity distribution function below.")
fig, ax = plt.subplots(nrows=1, ncols=2, dpi=200)
for i in [0, 1]:
    hist, bin_edges = np.histogram(u[i][~np.isnan(u[i])], density=True)
    ax[0].plot(bin_edges[:-1], hist)
    hist, bin_edges = np.histogram(v[i][~np.isnan(v[i])], density=True)
    ax[1].plot(bin_edges[:-1], hist)
ax[0].set_xlabel("u")
ax[1].set_xlabel("v")
ax[0].set_ylabel("PDF")
fig.savefig(os.path.join("img", "compare_vprofile.jpg"))
# %% codecell
print("The two methods show statistically very similar results")
print("Test the speed of the two methods.")
t = []
t.append(time.monotonic())
for func in [PIV_masked_1, PIV_masked_2]:
    x1, y1, u1, v1 = func(I0, I1, winsize, overlap, dt, mask)
    t.append(time.monotonic())
t1 = t[1] - t[0]
t2 = t[2] - t[1]
plt.bar([1, 2], [t1, t2])
plt.xticks([1, 2])
plt.ylabel("time (s)")
plt.savefig(os.path.join("img", "compare_time.jpg"))
print("The second method takes longer time. So the first method is better.")
print("Since it gives similar results while using less time.")
# %% codecell
# an example of flexible mask
from pivLib import PIV_masked
I20 = io.imread(os.path.join("img", "I20.tif"))
I21 = io.imread(os.path.join("img", "I21.tif"))
mask2 = io.imread(os.path.join("img", "mask2.tif"))
x, y, u, v = PIV_masked(I20, I21, 20, 10, 0.02, mask2)

fig, ax = plt.subplots()
ax.imshow(I20, cmap='gray')
ax.quiver(x, y, u, v, color='yellow')
ax.axis('off')
fig.savefig(os.path.join("img", "flex_mask_piv.jpg"))
