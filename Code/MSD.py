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
data.scatter_0(mode=None, highlight_Chile_data=False)
# %% codecell
data.scatter_1()
# %% codecell
data.plot_0(nbins=6, overlap=0.5, mode="lin")
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
