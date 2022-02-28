# %% codecell
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from skimage import io
from myImageLib import bestcolor, dirrec
from de_utils import *
from corrLib import readdata
from scipy.signal import savgol_filter
import trackpy as tp
# %% codecell
log_dir = r"..\Data\structured_log_DE.ods"
log = pd.read_excel(io=log_dir, sheet_name="main")
data = de_data(log)
# %% codecell
data.parameter_space(highlight_Chile_data=True)
# %% codecell
traj_folder = r"..\Data\traj"
data.look_for_missing_traj(traj_folder, fmt="{:02d}.csv")
# %% codecell
data.scatter_0()
# %% codecell
data.scatter_1()
# %% codecell
data.plot_0(nbins=6, overlap=0.5)
# %% codecell
data.plot_1(nbins=6, overlap=1, mode="log")
# %% codecell
data.Rinf2_tau()
# %% codecell
data.Rinf2_over_tau()
# %% codecell
data.rescale_Rinf_OD()
# %% codecell
data.rescale_Rinf_freespace()
# %% codecell
20/0.9
# %% codecell
np.mgrid[0:2, 0:3].shape
# %% codecell
data.parameter_space(highlight_Chile_data=True) # 1
data.scatter_0(mode="log", highlight_Chile_data=True) # 2
data.plot_MSD_model_Cristian() # 3
data.plot_0(nbins=5, overlap=0, mode="log") # 4
data.scatter_1(mode="log", highlight_Chile_data=True) # 5
data.plot_1(nbins=5, overlap=0, mode="log") # 6
data.Rinf2_tau() # 7
data.Rinf2_over_tau() # 8
data.rescale_Rinf_OD() # 9
data.rescale_Rinf_freespace() # 10
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
