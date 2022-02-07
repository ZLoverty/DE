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
log_dir = r"..\Data\structured_log_DE.ods"
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
# review data after 1026
log_dir = r"..\Data\structured_log_DE.ods"
log = pd.read_excel(io=log_dir, sheet_name="main")
log.head()
# %% codecell

# %% codecell
viridis = plt.cm.get_cmap('viridis')
plt.figure(dpi=150)
plt.scatter(log.OD, log.index, s=2, c=log.index, cmap=viridis)
plt.xlabel("OD")
plt.ylabel("arbitrary index")
plt.grid(ls=":")
# %% codecell
log1 = log.loc[(log.OD>=50)&(log.OD<=70)]
log1 = log1.sort_values("DE#")
log1
# %% codecell
viridis = plt.cm.get_cmap('viridis')
plt.figure(dpi=150)
plt.scatter(log1.D/log1.d, log1.d, s=15, c="black")
plt.xlabel("$D/d$")
plt.ylabel("$d$ ($\mu$m)")
plt.grid(ls=":")
# %% codecell
data_dir = r"..\Data\traj_50"
viridis = plt.cm.get_cmap('Set3', 5)
count = 0
plt.figure(dpi=200)
for num, i in log1.iterrows():
    traj = pd.read_csv(os.path.join(data_dir, "{:02d}.csv".format(i["DE#"])))
    msd = tp.msd(traj, mpp=i.MPP, fps=i.FPS/50, max_lagtime=len(traj)//10)
    plt.plot(msd.lagt, msd["<y^2>"], label=i["DE#"], color=viridis(count))
    count += 1
    if count > 4:
        plt.legend(bbox_to_anchor=(1,1), fontsize=5)
        plt.xlabel("$\Delta t$ (s)")
        plt.ylabel(r"$\left< \Delta y^2 \right>$ ($\mu$m$^2$)")
        plt.grid(which="both", ls=":")
        plt.loglog()
        plt.figure(dpi=200)
        count = 0
plt.legend(bbox_to_anchor=(1,1), fontsize=5)
plt.xlabel("$\Delta t$ (s)")
plt.ylabel(r"$\left< \Delta y^2 \right>$ ($\mu$m$^2$)")
plt.grid(which="both", ls=":")
plt.loglog()
# %% codecell
# plot all together and rescale with (D-d)^2
log_dir = r"..\Data\structured_log_DE.ods"
log = pd.read_excel(io=log_dir, sheet_name="main")
log1 = log.loc[(log.OD>=50)&(log.OD<=70)]
data_dir = r"..\Data\traj_50"
viridis = plt.cm.get_cmap('viridis', len(log1))
count = 0
plt.figure(dpi=200)
for num, i in log1.iterrows():
    traj = pd.read_csv(os.path.join(data_dir, "{:02d}.csv".format(i["DE#"])))
    msd = tp.msd(traj, mpp=i.MPP, fps=i.FPS/50, max_lagtime=len(traj)//10)
    plt.plot(msd.lagt/i["t2"], msd["<y^2>"]/i["Rinfy"], label=i["DE#"], color=viridis(count))
    count += 1
plt.legend(bbox_to_anchor=(1,1), fontsize=5)
plt.xlabel("$\Delta t/\\tau^*$")
plt.ylabel(r"$\left< \Delta y^2 \right> / R^\infty$")
plt.grid(which="both", ls=":")
plt.loglog()
# %% codecell
# plot Rinf vs. D
be = range(50, 250, 50)
D_list = []
Derr_list = []
R_list = []
Rerr_list = []
t_list = []
terr_list = []
for b in be:
    log2 = log1.loc[(log1.D>=b)&(log1.D<b+50)]
    D_list.append(log2.D.mean())
    Derr_list.append(log2.D.std())
    R_list.append(log2.Rinfy.mean())
    Rerr_list.append(log2.Rinfy.std())
    t_list.append(log2.t2.mean())
    terr_list.append(log2.t2.std())
plt.figure(dpi=150)
plt.errorbar(D_list, R_list, xerr=Derr_list, yerr=Rerr_list, ls="", color="black", marker="s")
plt.xlabel("$\left<D\\right>$ ($\mu$m)")
plt.ylabel("$R^\infty$ ($\mu$m$^2$)")
plt.twinx()
plt.errorbar(D_list, t_list, xerr=Derr_list, yerr=terr_list, ls="", color="red", marker="s")
plt.ylabel("$\\tau^*$ (s)")
# %% codecell
# D/d
be = range(2, 12, 2)
D_list = []
Derr_list = []
R_list = []
Rerr_list = []
t_list = []
terr_list = []
for b in be:
    r = log1.D / log1.d
    log2 = log1.loc[(r>=b)&(r<b+2)]
    r2 =  log2.D / log2.d
    D_list.append(r2.mean())
    Derr_list.append(r2.std())
    R_list.append(log2.Rinfy.mean())
    Rerr_list.append(log2.Rinfy.std())
    t_list.append(log2.t2.mean())
    terr_list.append(log2.t2.std())
plt.figure(dpi=150)
plt.errorbar(D_list, R_list, xerr=Derr_list, yerr=Rerr_list, ls="", color="black", marker="s")
plt.xlabel("$\left<D/d\\right>$")
plt.ylabel("$R^\infty$ ($\mu$m$^2$)")
plt.twinx()
plt.errorbar(D_list, t_list, xerr=Derr_list, yerr=terr_list, ls="", color="red", marker="s")
plt.ylabel("$\\tau^*$ (s)")
# %% codecell
# d
be = range(10, 60, 10)
D_list = []
Derr_list = []
R_list = []
Rerr_list = []
t_list = []
terr_list = []
for b in be:
    log2 = log1.loc[(log1.d>=b)&(log1.d<b+10)]
    D_list.append(log2.d.mean())
    Derr_list.append(log2.d.std())
    R_list.append(log2.Rinfy.mean())
    Rerr_list.append(log2.Rinfy.std())
    t_list.append(log2.t2.mean())
    terr_list.append(log2.t2.std())
plt.figure(dpi=150)
plt.errorbar(D_list, R_list, xerr=Derr_list, yerr=Rerr_list, ls="", color="black", marker="s")
plt.xlabel("$\left<d\\right>$ ($\mu$m)")
plt.ylabel("$R^\infty$ ($\mu$m$^2$)")
plt.twinx()
plt.errorbar(D_list, t_list, xerr=Derr_list, yerr=terr_list, ls="", color="red", marker="s")
plt.ylabel("$\\tau^*$ (s)")
# %% codecell
log1.loc[(log1.d>=10)&(log1.d<20)]
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
