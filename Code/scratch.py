from deLib import droplet_image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from myImageLib import readdata
import os
import json
from pivLib import piv_data
import scipy
from deLib import de_data
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
folder = r"C:\Users\liuzy\Documents\01192022\velocity_autocorr"
ac = pd.read_csv(os.path.join(folder, "00.csv")).set_index("t")
fig, ax = plt.subplots(figsize=(3.5, 3), dpi=100)
ax.plot(ac.index, ac.corrx)
ax.plot(ac.index, ac.corry)
ax.set_xlim([0, 2])
# %% codecell
folder = r"C:\Users\liuzy\Documents\01192022\velocity_autocorr"
ac = pd.read_csv(os.path.join(folder, "01.csv")).set_index("t")
fig, ax = plt.subplots(figsize=(3.5, 3), dpi=100)
ax.plot(ac.index, ac.corrx)
ax.plot(ac.index, ac.corry)
ax.set_xlim([0, 2])
# %% codecell
folder = r"C:\Users\liuzy\Documents\01192022\velocity_autocorr"
ac = pd.read_csv(os.path.join(folder, "02.csv")).set_index("t")
fig, ax = plt.subplots(figsize=(3.5, 3), dpi=100)
ax.plot(ac.index, ac.corrx)
ax.plot(ac.index, ac.corry)
ax.set_xlim([0, 2])
# %% codecell
folder = r"C:\Users\liuzy\Documents\01192022\velocity_autocorr"
ac = pd.read_csv(os.path.join(folder, "04.csv")).set_index("t")
fig, ax = plt.subplots(figsize=(3.5, 3), dpi=100)
ax.plot(ac.index, ac.corrx)
ax.plot(ac.index, ac.corry)
ax.set_xlim([0, 2])
# %% codecell
folder = r"C:\Users\liuzy\Documents\01192022\velocity_autocorr"
ac = pd.read_csv(os.path.join(folder, "05.csv")).set_index("t")
fig, ax = plt.subplots(figsize=(3.5, 3), dpi=100)
ax.plot(ac.index, ac.corrx)
ax.plot(ac.index, ac.corry)
ax.set_xlim([0, 3])
# %% codecell
folder = r"C:\Users\liuzy\Documents\01192022\velocity_autocorr"
ac = pd.read_csv(os.path.join(folder, "06.csv")).set_index("t")
fig, ax = plt.subplots(figsize=(3.5, 3), dpi=100)
ax.plot(ac.index, ac.corrx)
ax.plot(ac.index, ac.corry)
ax.set_xlim([0, 3])
# %% codecell
folder = r"C:\Users\liuzy\Documents\01192022\velocity_autocorr"
ac = pd.read_csv(os.path.join(folder, "07.csv")).set_index("t")
fig, ax = plt.subplots(figsize=(3.5, 3), dpi=100)
ax.plot(ac.index, ac.corrx)
ax.plot(ac.index, ac.corry)
ax.set_xlim([0, 3])
# %% codecell
folder = r"C:\Users\liuzy\Documents\01192022\velocity_autocorr"

fig, ax = plt.subplots(figsize=(3.5, 3), dpi=100)
for i in range(0, 7):
    ac = pd.read_csv(os.path.join(folder, "{:02d}.csv".format(i))).set_index("t")
    ax.plot(ac.index, ac.corrx, label=i)
    # ax.plot(ac.index, ac.corry)
ax.set_xlim([0, 3])
ax.legend()
# %% codecell
x = np.linspace(0, 1)
y = x * np.sqrt(1-x**2)
y1 = x
y3 = x - 0.5 * x ** 3
dv = (y1 - y) / y
dv3 = (y3 - y) / y
plt.plot(x, dv, label=1)
plt.plot(x, dv3, label=3)
# %% codecell
pd.DataFrame({"x": x, "dv": dv3})
# %% codecell
log = pd.read_excel(r"..\Data\structured_log_DE.ods", sheet_name="OD40-80_Paris")
dd = de_data(log)
# %% codecell
plt.scatter(log["(D-d)/d^2"], log["Max displacement"])
plt.loglog()
# %% codecell
traj_folder = r"..\Data\traj"
for num, i in log.iterrows():
    traj = pd.read_csv(os.path.join(traj_folder, "{:02d}.csv".format(i["DE#"])))
    # plt.plot(traj.x, traj.y)
    # plt.scatter(traj.x.mean(), traj.y.mean(), color="red", s=1000)
    #
    # break
    max_disp = (traj.y.max() - traj.y.mean()) * i.MPP / (i.D - i.d) * 2
    print(i["DE#"], max_disp)
# %% codecell
n = 40
traj = pd.read_csv(os.path.join(traj_folder, "{:02d}.csv".format(n)))
plt.plot(traj.x, traj.y)
plt.scatter(traj.x.mean(), traj.y.mean(), color="red", s=1000)
# %% codecell
log = pd.read_excel(r"..\Data\structured_log_DE.ods", sheet_name="OD40-80_Paris")
log = log.loc[log.Remove!=1]
bin_starts = range(40, 80, 10)
fig, ax = plt.subplots(figsize=(3.5, 3), dpi=200)
set1 = plt.cm.get_cmap("Set1")
for num, start in enumerate(bin_starts):
    log1 = log.loc[(log["OD"]>=start)&(log["OD"]<start+10)]
    log2 = log1.loc[log1["Max displacement"]<=0.56]
    log3 = log1.loc[log1["Max displacement"]>0.56]
    ax.scatter(log2["(D-d)/d^2"], log2["Rinfy"], marker="o",
                color=set1(num), label="{0:d}-{1:d}".format(start, start+10))
    ax.scatter(log3["(D-d)/d^2"], log3["Rinfy"], marker="^",
                color=set1(num))
log4 = log.loc[log["Leave surface"]=="Yes"]
ax.scatter(log4["(D-d)/d^2"], log4["Rinfy"], marker="o", s=100,
            edgecolor="black", facecolor=(0,0,0,0), lw=.5)
# for num, i in log.iterrows():
#     ax.annotate(i["DE#"], (i["(D-d)/d^2"], i["Rinfy"]), fontsize=5)
ax.legend(fontsize=8)
ax.loglog()
ax.set_xlim([0.01, 2])
ax.set_ylim([1, 1500])
ax.set_xlabel("$(D-d)/d^2$")
ax.set_ylabel("$R^2_\infty$ ($\mu$m$^2$)")
ax.grid(which="both", ls=":")

# %% codecell
log = pd.read_excel(r"..\Data\structured_log_DE.ods", sheet_name="OD40-80_Paris")
log = log.loc[log.Remove!=1]
bin_starts = range(40, 80, 10)
fig, ax = plt.subplots(figsize=(3.5, 3), dpi=200)
set1 = plt.cm.get_cmap("Set1")
for num, start in enumerate(bin_starts):
    log1 = log.loc[(log["OD"]>=start)&(log["OD"]<start+10)]
    log2 = log1.loc[log1["Max displacement"]<=0.56]
    log3 = log1.loc[log1["Max displacement"]>0.56]
    ax.scatter(log2["(D-d)/d^2"], log2["t2"], marker="o",
                color=set1(num), label="{0:d}-{1:d}".format(start, start+10))
    ax.scatter(log3["(D-d)/d^2"], log3["t2"], marker="^",
                color=set1(num))
log4 = log.loc[log["Leave surface"]=="Yes"]
ax.scatter(log4["(D-d)/d^2"], log4["t2"], marker="o", s=100,
            edgecolor="black", facecolor=(0,0,0,0), lw=.5)
ax.legend(fontsize=8)
ax.loglog()
ax.set_xlim([0.01, 2])
ax.set_ylim([1, 20])
ax.set_xlabel("$(D-d)/d^2$")
ax.set_ylabel("$\\tau^*$ (s)")
ax.grid(which="both", ls=":")
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
