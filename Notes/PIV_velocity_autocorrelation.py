# %% codecell
# load data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from corrLib import xy_bin

data_folder = r'C:\Users\liuzy\Data\DE\12092021\velocity_autocorr'
vac = []
for i in range(0, 25):
    data_file = os.path.join(data_folder, "{:02d}".format(i), "vac_data.csv")
    vac.append(pd.read_csv(data_file))

# %% codecell
bounds = [0, 7, 11, 19, 25]
for j in range(4):
    plt.figure(dpi=200)
    for i in range(bounds[j], bounds[j+1]):
        plt.plot(vac[i].t, vac[i].vac, label=i)
        plt.xlim([0,150])
        plt.xlabel("t (frame)")
        plt.ylabel("VACF")
    plt.legend()
    plt.savefig(os.path.join("img", "VACF-{}.jpg".format(j)))


125 * 0.16

341 * 0.16
