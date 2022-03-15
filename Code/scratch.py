from deLib import droplet_image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from myImageLib import readdata
import os
import json
from pivLib import piv_data
import scipy
# %% codecell
folder = r"C:\Users\liuzy\Documents\01192022"
image_folder = os.path.join(folder, "02", "8-bit")
l = readdata(image_folder, "tif")
DI = droplet_image(l)
# %% codecell
piv_folder = os.path.join(folder, "moving_mask_piv", "02")
piv_params = pd.read_json(os.path.join(piv_folder, "piv_params.json"))
out_folder = os.path.join(folder, "piv_overlay_moving", "02")
traj = pd.read_json(os.path.join(piv_folder, "droplet_traj.json"))
with open(os.path.join(piv_folder, "piv_params.json"), "r") as f:
    piv_params = json.load(f)
DI.piv_overlay_moving(piv_folder, out_folder, traj, piv_params)
# %% codecell
piv_folder = os.path.join(folder, "piv_drop", "02")
out_folder = os.path.join(folder, "piv_overlay", "02")
DI.piv_overlay_fixed(piv_folder, out_folder, sparcity=1)
# %% codecell
piv_folder = os.path.join(folder, "piv_drop", "02")
l = readdata(piv_folder, "csv")
piv = piv_data(l)
mv = piv.mean_velocity(plot=True)
# %% codecell
piv_folder = os.path.join(folder, "moving_mask_piv", "02")
l = readdata(piv_folder, "csv")
piv1 = piv_data(l)
mv1 = piv1.mean_velocity(plot=True)
# %% codecell
fig, ax = plt.subplots(figsize=(3.5, 3), dpi=100)
ax.plot(mv.t, scipy.ndimage.gaussian_filter(mv.v_mean, 100/4)*0.16, label="fixed")
ax.plot(mv1.t, scipy.ndimage.gaussian_filter(mv1.v_mean, 100/4)*0.16, label="moving")
ax.legend(frameon=False)
ax.set_xlabel("time (s)")
ax.set_ylabel("mean velocity (um/s)")
# %% codecell
scipy.ndimage.gaussian_filter(mv.v_mean, 1000/4)
# %% codecell
piv.vacf(plot=True, xlim=[0, 3])
# %% codecell
piv1.vacf(plot=True, xlim=[0, 3])
# %% codecell
cs = piv.corrS1d(n=100, plot=True)
# %% codecell
cs1 = piv1.corrS1d(n=100, plot=True)
# %% codecell
fig, ax = plt.subplots(figsize=(3.5, 3), dpi=100)
ax.plot(cs.R*0.16, scipy.ndimage.gaussian_filter(cs.C, 0/4), label="fixed")
ax.plot(cs1.R*0.16, scipy.ndimage.gaussian_filter(cs1.C, 0/4), label="moving")
ax.legend(frameon=False)
ax.set_xlabel("distance (um)")
ax.set_ylabel("spatial correlation")
ax.set_xlim([0, 50])
# %% codecell
cs
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
