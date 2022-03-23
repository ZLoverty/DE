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
from corrLib import autocorr1d
from openpiv.smoothn import smoothn

folder = r"C:\Users\liuzy\Documents\01192022"

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
ax.set_xlabel("$\Delta t$ (s)")
ax.set_ylabel("VACF")

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
def vacf(uvstack, dt=0.04, mode="direct", smooth_method="gaussian", smooth_window=3, xlim=None, plot=False):
    """Compute averaged vacf from PIV data.
    This is a wrapper of function autocorr1d(), adding the averaging over all the velocity spots.
    Args:
    mode -- the averaging method, can be "direct" or "weighted".
            "weighted" will use mean velocity as the averaging weight, whereas "direct" uses 1.
    smooth_window -- window size for gaussian smoothing in time
    xlim -- xlim for plotting the VACF, does not affect the return value
    Returns:
    corrData -- DataFrame of (t, corrx, corry)
    """
    # rearrange vstack from (f, h, w) to (f, h*w), then transpose
    corr_components = []
    for name, stack in zip(["corrx", "corry"], uvstack):
        stack_r = stack.reshape((stack.shape[0], -1)).T
        stack_r = stack_r[~np.isnan(stack_r).any(axis=1)]
        if smooth_method == "gaussian":
            stack_r = scipy.ndimage.gaussian_filter(stack_r, (0, smooth_window/4))
        elif smooth_method == "smoothn":
            stack_r = smoothn(stack_r, axis=1)[0]
        # compute autocorrelation
        corr_list = []
        weight = 1
        normalizer = 0
        for x in stack_r:
            if np.isnan(x[0]) == False: # masked out part has velocity as nan, which cannot be used for correlation computation
                if mode == "weighted":
                    weight = abs(x).mean()
                corr = autocorr1d(x) * weight
                if np.isnan(corr.sum()) == False:
                    normalizer += weight
                    corr_list.append(corr)
        corr_mean = np.nansum(np.stack(corr_list, axis=0), axis=0) / normalizer
        corr_components.append(pd.DataFrame({"c": corr_mean, "t": np.arange(len(corr_mean)) * dt}).set_index("t").rename(columns={"c": name}))
    ac = pd.concat(corr_components, axis=1)
    return ac
# %% codecell
folder = r"C:\Users\liuzy\Documents\01192022\moving_mask_piv\06"
l = readdata(folder, "csv")
piv = piv_data(l, cutoff=1000)
# uvstack = piv.load_stack(cutoff=1000)
# %% codecell
corr_components = []
smooth_window = 3
for name, stack in zip(["corrx", "corry"], uvstack):
    # stack = scipy.ndimage.gaussian_filter(stack, (smooth_window/4,0,0))
    # stack = smoothn(stack, axis=0)[0]
    # stack = smoothn(stack)[0]
    stack_r = stack.reshape((stack.shape[0], -1)).T
    stack_r = stack_r[~np.isnan(stack_r).any(axis=1)]
    stack_r = smoothn(stack_r, axis=1)[0]
    # compute autocorrelation
    corr_list = []
    weight = 1
    normalizer = 0
    for x in stack_r:
        if np.isnan(x.mean()) == False and x.mean() != 0: # masked out part has velocity as nan, which cannot be used for correlation computation
            # x = smoothn(x)[0]
            corr = autocorr1d(x) * weight
            if np.isnan(corr.sum()) == False:
                normalizer += weight
                corr_list.append(corr)
    corr_mean = np.nansum(np.stack(corr_list, axis=0), axis=0) / normalizer
    corr_components.append(pd.DataFrame({"c": corr_mean, "t": np.arange(len(corr_mean)) * 0.04}).set_index("t").rename(columns={"c": name}))
acn = pd.concat(corr_components, axis=1)
# %% codecell
# ac.plot()
plt.plot(acn.index, acn.mean(axis=1))
plt.xlim([0, 3])
# %% codecell
x.shape
stack_r.shape
smoothn(x)

# %% codecell
plt.figure(dpi=150)
sws = range(0, 50, 10)
colors = plt.cm.get_cmap("viridis", len(sws))
for num, sw in enumerate(sws):
    ac = piv.vacf(smooth_window=sw)
    plt.plot(ac.index, ac.mean(axis=1), color=colors(num), label=sw, lw=1)
acn = piv.vacf(uvstack, smooth_method="smoothn")
plt.plot(acn.index, acn.mean(axis=1), color="red", label="smoothn", lw=2)
plt.xlim(0, 5)
plt.xlabel("$\Delta t$ (s)")
plt.ylabel("VACF")
plt.legend()
# %% codecell
folder = r"C:\Users\liuzy\Documents\01192022\moving_mask_piv\06"
l = readdata(folder, "csv")
piv = piv_data(l, cutoff=1000)
# %% codecell
# review vacf data
n = 0


# %% codecell
folder = r"C:\Users\liuzy\Documents\01172022\velocity_autocorr"
l = readdata(folder, "csv")
for num, i in l.iterrows():
    if num % 6 == 0:
        plt.figure()
        plt.xlim(0, 3)
    ac = pd.read_csv(i.Dir).set_index("t")
    plt.plot(ac.index, ac.mean(axis=1), label=i.Name)
    if num % 6 == 5:
        plt.legend()





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
