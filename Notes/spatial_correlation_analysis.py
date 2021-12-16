# %% codecell
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from corrLib import readdata, distance_corr, xy_bin
from matplotlib import cm
# %% codecell
folder = r"C:\Users\liuzy\Data\DE\12092021\spatial_correlation\21"
l = readdata(folder, "csv")
viridis = cm.get_cmap('viridis', len(l))
for num, i in l[::10].iterrows():
    data = pd.read_csv(i.Dir)
    dc = distance_corr(data.X, data.Y, data.CV)
    x, y = xy_bin(dc.R, dc.C, n=10)
    plt.plot(x, y, marker='o', color=viridis(num), label=i.Name.split('-')[0])
plt.legend(bbox_to_anchor=(1, 1))
plt.xlabel("r (um)")
plt.ylabel("velocity correlation")
# %% codecell
# animation
folder = r"C:\Users\liuzy\Data\DE\12092021\spatial_correlation\21"
l = readdata(folder, "csv")
viridis = cm.get_cmap('viridis', len(l))
fig, ax = plt.subplots(dpi=150)
for num, i in l[::10].iterrows():
    data = pd.read_csv(i.Dir)
    dc = distance_corr(data.X, data.Y, data.CV)
    x, y = xy_bin(dc.R, dc.C, n=10)
    ax.plot(x, y, marker='o', color=viridis(num))
    ax.set_title(i.Name.split('-')[0])
    ax.set_xlabel("r (px)")
    ax.set_ylabel("velocity correlation")
    plt.pause(0.3)

# impossible with just plt
data
# %% codecell
fig, ax = plt.subplots(dpi=150)
axis = ax.plot([], [])
ax.set_xlim([])
def animate(i, l):

y


# %% codecell

# %% codecell
