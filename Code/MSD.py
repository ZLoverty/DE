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
# %% codecell
# review data after 1026
log_dir = r"..\Data\structured_log_DE.ods"
log = pd.read_excel(io=log_dir, sheet_name="main")
log.head()
# %% codecell
OD_min = 20
OD_max = 40
log1 = log.loc[(log.OD>=OD_min)&(log.OD<=OD_max)]
r = (log1.D - log1.d) / log1.d ** 2
plt.scatter(r, log1["DE#"])
plt.xlabel("$(D-d)/d^2$")
plt.ylabel("DE index")
# %% codecell
# visualize the bins
log1 = log.loc[(log.OD>=OD_min)&(log.OD<=OD_max)]
r = (log1.D - log1.d) / log1.d ** 2
plt.scatter(r, log1["DE#"])
plt.xlabel("$(D-d)/d^2$")
plt.ylabel("DE index")
N = 5
range_size = r.max() - r.min()
bin_size = range_size / N * 2
bin_start = np.linspace(r.min(), r.max()-bin_size, N)
bin_end = bin_start + bin_size
count = 20
for start, end in zip(bin_start, bin_end):
    plt.plot([start, end], [count, count])
    count += 2

# %% codecell
# Make ranges for r
log1 = log.loc[(log.OD>=OD_min)&(log.OD<=OD_max)]
r = (log1.D - log1.d) / log1.d ** 2
N = 5
range_size = r.max() - r.min()
bin_size = range_size / N * 1.5
bin_start = np.linspace(r.min(), r.max()-bin_size, N)
bin_end = bin_start + bin_size
for start, end in zip(bin_start, bin_end):
    print(start, end)
    log2 = log1.loc[(r>=start)&(r<=end)]
    r2 = (log2.D - log2.d) / log2.d ** 2
    plt.errorbar(r2.mean(), (log2.Rinfy**0.5).mean(), xerr=r2.std(), yerr=(log2.Rinfy**0.5).std(), marker="o")
plt.xlabel("$(D-d)/d^2$")
plt.ylabel("$R_\infty$")
# plt.xlim([0, 1.2])
# plt.ylim([0, 35])
#

# %% codecell
bin_start
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
plt.figure(dpi=150)
plt.scatter(log1.D-log1.d, log1.d, s=15, c="black")
plt.xlabel("$D-d$")
plt.ylabel("$d$ ($\mu$m)")
plt.grid(ls=":")
# %% codecell
log1 = log.loc[log["DE#"]<23]
data_dir = r"..\Data\traj"
viridis = plt.cm.get_cmap('Set3', 5)
count = 0
plt.figure(dpi=200)
for num, i in log1.iterrows():
    traj_dir = os.path.join(data_dir, "{:03d}.csv".format(i["DE#"]))
    if os.path.exists(traj_dir):
        traj = pd.read_csv(traj_dir)
    else:
        print("Missing traj {:d}".format(i["DE#"]))
    msd = tp.msd(traj, mpp=i.MPP, fps=i.FPS, max_lagtime=len(traj)//5)
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
# plt.savefig("collapse_msd.pdf")
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
    R_list.append((log2.Rinfy**0.5).mean())
    Rerr_list.append((log2.Rinfy**0.5).std())
    t_list.append(log2.t2.mean())
    terr_list.append(log2.t2.std())
plt.figure(figsize=(3,4),dpi=150)
plt.errorbar(D_list, R_list, xerr=Derr_list, yerr=Rerr_list, ls="", color="black", marker="o",
                label="$R^\infty$", markersize=10)
plt.xlabel("$\left<D\\right>$ ($\mu$m)")
plt.ylabel("$R^\infty$ ($\mu$m)")
plt.legend(frameon=False, bbox_to_anchor=(1, 1))
plt.twinx()
ax = plt.gca()
ax.yaxis.label.set_color('red')
ax.tick_params(axis="y", color="red", labelcolor="red")
ax.spines['right'].set_color('red')
plt.errorbar(D_list, t_list, xerr=Derr_list, yerr=terr_list, ls="", color="red", marker="s",
                label="$\\tau^*$")
plt.ylabel("$\\tau^*$ (s)")
plt.legend(frameon=False, bbox_to_anchor=(1, 0.9))
# plt.savefig("RTDo.pdf")

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
    R_list.append((log2.Rinfy**0.5).mean())
    Rerr_list.append((log2.Rinfy**0.5).std())
    t_list.append(log2.t2.mean())
    terr_list.append(log2.t2.std())
plt.figure(figsize=(4,4), dpi=150)
plt.errorbar(D_list, R_list, xerr=Derr_list, yerr=Rerr_list, ls="", color="black", marker="o",
                markersize=10)
plt.xlabel("$\left<D/d\\right>$")
plt.ylabel("$R^\infty$ ($\mu$m)")
plt.ylim([0, 35])
plt.twinx()
ax = plt.gca()
ax.yaxis.label.set_color('red')
ax.tick_params(axis="y", color="red", labelcolor="red")
ax.spines['right'].set_color('red')
plt.errorbar(D_list, t_list, xerr=Derr_list, yerr=terr_list, ls="", color="red", marker="s")
plt.ylabel("$\\tau^*$ (s)")
plt.xlim([0, 11])
plt.ylim([0, 17])
# plt.savefig("RTDd.pdf")
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
    R_list.append((log2.Rinfy**0.5).mean())
    Rerr_list.append((log2.Rinfy**0.5).std())
    t_list.append(log2.t2.mean())
    terr_list.append(log2.t2.std())
plt.figure(figsize=(4,4), dpi=150)
plt.errorbar(D_list, R_list, xerr=Derr_list, yerr=Rerr_list, ls="", color="black", marker="o",
                markersize=10)
plt.xlabel("$\left<d\\right>$ ($\mu$m)")
plt.ylabel("$R^\infty$ ($\mu$m)")
plt.ylim([0, 30])
plt.twinx()
ax = plt.gca()
ax.yaxis.label.set_color('red')
ax.tick_params(axis="y", color="red", labelcolor="red")
ax.spines['right'].set_color('red')
plt.errorbar(D_list, t_list, xerr=Derr_list, yerr=terr_list, ls="", color="red", marker="s")
plt.ylabel("$\\tau^*$ (s)")
plt.xlim([0, 60])
plt.ylim([0, 16])
# plt.savefig("RTdi.pdf")
# %% codecell
log1.loc[(log1.d>=10)&(log1.d<20)]
# %% codecell
# Rinf vs. D/d
log_dir = r"..\Data\structured_log_DE.ods"
log = pd.read_excel(io=log_dir, sheet_name="main")
log1 = log.loc[(log.OD>=50)&(log.OD<=70)]
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
    R_list.append((log2.Rinfy**0.5).mean())
    Rerr_list.append((log2.Rinfy**0.5).std())
    t_list.append(log2.t2.mean())
    terr_list.append(log2.t2.std())
plt.figure(figsize=(3,4), dpi=150)
plt.errorbar(D_list, R_list, xerr=Derr_list, yerr=Rerr_list, ls="", color="black", marker="o",
                markersize=10)
plt.xlabel("$\left<D/d\\right>$")
plt.ylabel("$R^\infty$ ($\mu$m)")
plt.xlim([0, 11])
plt.ylim([0, 34])
plt.twinx()
ax = plt.gca()
ax.yaxis.label.set_color('red')
ax.tick_params(axis="y", color="red", labelcolor="red")
ax.spines['right'].set_color('red')
plt.errorbar(D_list, t_list, xerr=Derr_list, yerr=terr_list, ls="", color="red", marker="s")
plt.ylabel("$\\tau^*$ (s)")
plt.ylim([0, 17])
# plt.savefig("RTDd.pdf")
# %% codecell
log_dir = r"..\Data\structured_log_DE.ods"
log = pd.read_excel(io=log_dir, sheet_name="main")
log1 = log.loc[(log.OD>=50)&(log.OD<=70)]
be = range(25, 225, 50)
D_list = []
Derr_list = []
R_list = []
Rerr_list = []
t_list = []
terr_list = []
for b in be:
    r = log1.D - log1.d
    log2 = log1.loc[(r>=b)&(r<b+50)]
    r2 =  log2.D - log2.d
    D_list.append(r2.mean())
    Derr_list.append(r2.std())
    R_list.append((log2.Rinfy**0.5).mean())
    Rerr_list.append((log2.Rinfy**0.5).std())
    t_list.append(log2.t2.mean())
    terr_list.append(log2.t2.std())
plt.figure(figsize=(3,4), dpi=150)
plt.errorbar(D_list, R_list, xerr=Derr_list, yerr=Rerr_list, ls="", color="black", marker="o",
                markersize=10)
plt.xlabel("$\left< D-d \\right>$")
plt.ylabel("$R^\infty$ ($\mu$m)")
plt.twinx()
ax = plt.gca()
ax.yaxis.label.set_color('red')
ax.tick_params(axis="y", color="red", labelcolor="red")
ax.spines['right'].set_color('red')
plt.errorbar(D_list, t_list, xerr=Derr_list, yerr=terr_list, ls="", color="red", marker="s")
plt.ylabel("$\\tau^*$ (s)")
# %% codecell
data_dir = r"../Data/traj_50"
traj = pd.read_csv(os.path.join(data_dir, "35.csv"))
traj.head()
plt.plot(traj.x, traj.y, alpha=0.5, lw=0.5)
plt.scatter(traj.x, traj.y, s=10, c=traj.frame, cmap="viridis")
plt.axis("equal")
# plt.savefig("traj-illu.pdf")
# %% codecell
# Rinf vs. tau
log_dir = r"..\Data\structured_log_DE.ods"
log = pd.read_excel(io=log_dir, sheet_name="main")
log1 = log.loc[(log.OD>=50)&(log.OD<=70)]
plt.figure(figsize=(3,3), dpi=150)
plt.scatter(log1.t2, log1.Rinfy)
# plt.xlim([0, 18])
# plt.ylim([0, 1200])
plt.xlabel("$\\tau^*$ (s)")
plt.ylabel("$R_\infty^2$ ($\mu$m)")
plt.xlim([0,17])
plt.ylim([0,1100])
# plt.savefig("Rinf_vs_tau.pdf")

# plt.loglog()
#

# %% codecell
data_dir = r"../Data/traj_50"
traj = pd.read_csv(os.path.join(data_dir, "35.csv"))
msd = tp.msd(traj, mpp=i.MPP, fps=i.FPS/50, max_lagtime=len(traj)//10)
plt.figure(figsize=(3,3))
plt.plot(msd.lagt, msd["<y^2>"], label=i["DE#"])
plt.loglog()
plt.xlabel("$\Delta t$")
plt.ylabel(r"$\left< \Delta y^2 \right>$")
plt.grid(which="both", ls=":")
# plt.savefig("msd-example.pdf")
# %% codecell
log1.OD.mean()
# %% codecell
log1.OD.std()
# %% codecell
log_dir = r"..\Data\structured_log_DE.ods"
log = pd.read_excel(io=log_dir, sheet_name="main")
log1 = log.loc[(log.OD>=50)&(log.OD<=70)]
be = np.linspace(0, 0.7,10)
D_list = []
Derr_list = []
R_list = []
Rerr_list = []
t_list = []
terr_list = []
for b in be:
    r = (log1.D-log1.d) / log1.d ** 2
    log2 = log1.loc[(r>=b)&(r<b+0.2)]
    r2 =  (log2.D-log2.d) / log2.d ** 2
    D_list.append(r2.mean())
    Derr_list.append(r2.std())
    R_list.append((log2.Rinfy**0.5).mean())
    Rerr_list.append((log2.Rinfy**0.5).std())
    t_list.append(log2.t2.mean())
    terr_list.append(log2.t2.std())
plt.figure(figsize=(3,4), dpi=150)
plt.errorbar(D_list, R_list, xerr=Derr_list, yerr=Rerr_list, ls="", color="black", marker="o",
                markersize=10)
plt.xlabel("$\left<(D-d)/d^2\\right>$")
plt.ylabel("$R^\infty$ ($\mu$m)")
# plt.xlim([0, 11])
plt.ylim([0, 34])
plt.twinx()
ax = plt.gca()
ax.yaxis.label.set_color('red')
ax.tick_params(axis="y", color="red", labelcolor="red")
ax.spines['right'].set_color('red')
plt.errorbar(D_list, t_list, xerr=Derr_list, yerr=terr_list, ls="", color="red", marker="s")
plt.ylabel("$\\tau^*$ (s)")
plt.ylim([0, 17])
# %% codecell
r = (log1.D-log1.d) / log1.d ** 2
plt.plot(r)
# %% codecell
log2
# %% codecell
r
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
