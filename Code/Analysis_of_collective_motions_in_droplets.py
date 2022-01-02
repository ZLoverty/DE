# This notebook make plots and demos for the note Analysis_of_collective_motions_in_droplets
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter
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

# %% markdown
$$\phi$$
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
    # avoid divided by 0
    r[1][r[1]==0] = np.nan

    y1 = - x1 * r[0] / r[1]
    length = (x1**2 + y1**2) ** 0.5
    return np.array([x1, y1]) / length
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
    point = (pivData.x, pivData.y)
    tu = tangent_unit(point, center)
    # \Sigma vt
    sum_vt = abs((pivData.u * tu[0] + pivData.v * tu[1])).sum()
    sum_v = ((pivData.u**2 + pivData.v**2) ** 0.5).sum()
    OP = (sum_vt/sum_v - 2/np.pi) / (1 - 2/np.pi)
    return OP


# %% codecell
from skimage import io
pivData = pd.read_csv(os.path.join("test_files", "00000-00001.csv"))
img = io.imread(os.path.join("test_files", "22.tif"))
center = (259, 227)
order_parameter_wioland2013(pivData, center)

# %% codecell
point = (pivData.x, pivData.y)
tu = tangent_unit(point, center)
plt.figure(dpi=150)
plt.imshow(img, cmap='gray')
plt.quiver(pivData.x, pivData.y, pivData.u, pivData.v, color='yellow', width=0.005)
plt.quiver(pivData.x, pivData.y, -tu[0], tu[1], color='red', width=0.0025)
# plt.axis('off')

# %% codecell
plt.quiver(pivData.x, pivData.y, tu[0], tu[1], color='red', width=0.0025)

# %% codecell


# %% codecell


# %% codecell


# %% codecell

# %% codecell


# %% codecell

# %% codecell
