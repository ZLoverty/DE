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
