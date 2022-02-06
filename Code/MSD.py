# %% codecell
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from skimage import io
from myImageLib import bestcolor, dirrec
from de_utils import *
from corrLib import readdata
from scipy.signal import savgol_filter
import trackpy as tp
import datetime
# %% codecell
# Old data MSD visualize
log_dir = r"..\Data\structured_log\structured_log_DE.ods"
log = pd.read_excel(io=log_dir, sheet_name="before10262021")
log.head()
# %% codecell
i = log.loc[0]
i.Date.strftime("%m%d%Y")
# %% codecell
folder = r"E:\DE"
traj = pd.read_csv(os.path.join(folder, i.Date.strftime("%m%d%Y"), i["Video#"], "crop_HoughCircles", "traj.csv"))
# %% codecell
traj = traj.assign(frame=traj.index, particle=0)
msd = tp.msd(traj, mpp=i.MPP, fps=i.FPS, max_lagtime=len(traj)//5)
# %% codecell
plt.plot(msd.lagt, msd["<y^2>"])
plt.loglog()
# %% codecell
log1 = log.loc[log.Date==datetime.datetime(2021, 8, 13)]
# %% codecell
plt.figure(dpi=200)
viridis = plt.cm.get_cmap("viridis", 8)
count = 0
for num, i in log1.iterrows():
    traj = pd.read_csv(os.path.join(folder, i.Date.strftime("%m%d%Y"), i["Video#"], "crop_HoughCircles", "traj.csv"))
    traj = traj.assign(frame=traj.index, particle=0)
    msd = tp.msd(traj, mpp=i.MPP, fps=i.FPS, max_lagtime=len(traj)//5)
    plt.plot(msd.lagt, msd["<y^2>"], label=i["Video#"], color=viridis(count))
    count += 1
    if count == 8:
        plt.legend(bbox_to_anchor=(1,1), fontsize=5)
        plt.xlabel("$\Delta t$ (s)")
        plt.ylabel(r"$\left< \Delta y^2 \right>$ ($\mu$m$^2$)")
        plt.grid(ls=":")
        plt.loglog()
        plt.figure(dpi=200)
        count = 0
plt.legend(bbox_to_anchor=(1,1), fontsize=5)
plt.xlabel("$\Delta t$ (s)")
plt.ylabel(r"$\left< \Delta y^2 \right>$ ($\mu$m$^2$)")
plt.grid(ls=":")
plt.loglog()

# %% codecell
dirrec(r"C:\Users\liuzy\Documents", "traj_50.csv")
# %% codecell
import shutil

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
