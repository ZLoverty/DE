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
from scipy.signal import correlate2d
from xcorr_funcs import *
from myImageLib import to8bit
from corrLib import readdata
from matplotlib.patches import Ellipse
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
class fixed_mask_PIV:
    def PIV_masked_1(self, I0, I1, winsize, overlap, dt, mask):
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
    def PIV_masked_2(self, I0, I1, winsize, overlap, dt, mask):
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
    def PIV_masked_3(self, I0, I1, winsize, overlap, dt, mask):
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
    def test(self):
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
        print("The second method takes longer time. So the first method is better.")
        print("Since it gives similar results while using less time.")
        I20 = io.imread(os.path.join("img", "I20.tif"))
        I21 = io.imread(os.path.join("img", "I21.tif"))
        mask2 = io.imread(os.path.join("img", "mask2.tif"))
        x, y, u, v = PIV_masked(I20, I21, 20, 10, 0.02, mask2)
        fig, ax = plt.subplots()
        ax.imshow(I20, cmap='gray')
        ax.quiver(x, y, u, v, color='yellow')
        ax.axis('off')

# %% codecell
# droplet trajectory -- corrTrack
import corrTrack
folder = r"C:\Users\liuzy\Documents\01192022"
img = io.imread(os.path.join(folder, "16", "raw", "14000.tif"))
mask = io.imread(os.path.join(folder, "mask", "16.tif"))
img8 = to8bit(img)
xy, pkv = corrTrack.track_spheres(img, mask, 1)
xy
# %% codecell
h, w = img.shape
offset = np.array([165, 173]) - np.array([h/2, w/2])
xy = xy.squeeze()
xy += offset
plt.imshow(img8)
plt.scatter(xy[1], xy[0], color="red")
# %% codecell
corr = correlate2d(img, mask, mode="same")

corr2 = normxcorr2(img, img, mode="same")


plt.imshow(corr)

plt.imshow(corr2)

xy

img.shape

# %% codecell
class droplet_image:
    """Container of functions related to confocal droplet images"""
    def __init__(self, image_sequence, mask=None, xy0=None, mask_shape=None):
        """image_sequence: dataframe of image dir info, readdata return value
        mask: image mask, the same as PIV mask
        xy0: 2-tuple of droplet initial coordinates, read from positions.csv file
        mask_shape: shape of the circular mask, 2-tuple specifying the rect bounding box of the mask, typically a square
                    read from positions.csv file"""
        self.sequence = image_sequence
        self.data = self.sequence.copy()
        self.mask = mask
        self.xy0 = np.array(xy0)
        self.mask_shape = np.array(mask_shape)
        self.process_first_image()
    def process_first_image(self):
        img = io.imread(self.sequence.Dir[0])
        h, w = img.shape
        xy, pkv = corrTrack.track_spheres(img, self.mask, 1, subpixel=True)
        self.xyc = np.flip(xy.squeeze())
        # The center coords should be very close to the image center (w/2, h/2)
        diff = np.square(self.xyc-np.array([w/2, h/2])).sum()
        if diff > 10: # this threshold is arbitrary
            print("The detected center is too far from the image center, check if the input is correct.")
        return diff
    def droplet_traj(self):
        xym_list = []
        for num, i in self.sequence.iterrows():
            img = io.imread(i.Dir)
            xy, pkv = corrTrack.track_spheres(img, self.mask, 1)
            xym_list.append(np.flip(xy.squeeze()))
        xym = np.stack(xym_list, axis=0)
        # Update the trajectory of droplet in self.data, also return self.data for external uses
        self.data = self.data.assign(x=self.xy0[0] + xym[:, 0] - self.xyc[0], y=self.xy0[1] + xym[:, 1] - self.xyc[1])
        return self.data
    def __len__(self):
        return len(self.sequence)
    def get_cropped_image(self, index):
        """Retrieve cropped image according to """
        imgDir = self.sequence.Dir[index]
        x = int(self.data.x[index])
        y = int(self.data.y[index])
        h, w = mask_shape
        x0 = x - w // 2
        x1 = x0 + w
        y0 = y - h // 2
        y1 = y0 + h
        img = io.imread(imgDir)
        cropped = img[y0:y1, x0:x1]
        return cropped
    def get_image(self, index):
        imgDir = self.sequence.Dir[index]
        img = io.imread(imgDir)
        return img
    def get_image_name(self, index):
        return self.sequence.Name[index]

# %% codecell
image_sequence = readdata(os.path.join(folder, "16", "raw"), "tif")[:1000]
mask = io.imread(os.path.join(folder, "mask", "16.tif"))
xy0 = (173, 165)
mask_shape = (174, 174)
di = droplet_image(image_sequence, mask, xy0, mask_shape)
len(di)
di.get_image_name(999)
# %% codecell
traj = di.droplet_traj()

# %% codecell
plt.imshow(img, cmap='gray')
plt.scatter(traj[:, 0], traj[:, 1])


# %% codecell
for num, i in traj[::100].iterrows():
    fig, ax = plt.subplots()
    img = io.imread(i.Dir)
    elli = Ellipse((i.x, i.y), 174, 174, facecolor=(0,0,0,0), lw=1, edgecolor="red")
    ax.imshow(img, cmap="gray")
    ax.add_patch(elli)

# %% codecell
cropped = di.get_cropped_image(1000)
plt.imshow(cropped, cmap="gray")
plt.axis("off")

# %% codecell
img = di.get_image(0)
plt.imshow(img, cmap="gray")
plt.axis("off")

# %% codecell
img = di.get_image(1000)
plt.imshow(img, cmap="gray")
plt.axis("off")

# %% codecell
# PIV
from pivLib import PIV
for i0, i1 in zip(di.sequence.index[::2], di.sequence.index[1::2]):
    I0 = di.get_cropped_image(i0)
    I1 = di.get_cropped_image(i1)
    x, y, u, v = PIV(I0, I1, 20, 10, 0.02)
    data = pd.DataFrame({"x": x.flatten(), "y": y.flatten(), "u": u.flatten(), "v": v.flatten()})
    data.to_csv(r"C:\Users\liuzy\Documents\01192022\moving_mask_piv\16\{0:05d}-{1:05d}.csv".format(i0, i1))

plt.imshow(I0, cmap="gray")
plt.quiver(x, y, u, v, color="yellow")
plt.axis("off")

# %% codecell
# test json
import json
data = {"string": "test", "list": [1,2,3]}
with open("test.json", "w") as fp:
    json.dump(data, fp)

# %% codecell
with open("test.json", "r") as fp:
    read = json.load(fp)
read
read["list"]
