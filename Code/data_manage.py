# %% codecell
import os
import pandas as pd
from corrLib import readdata
from utils import *
import numpy as np
import matplotlib.pyplot as plt
from myImageLib import dirrec
from shutil import copy
# %% markdown
# ## 1 Manage the main log
#
# Run the cell below to know what has or has not been done!
# %% codecell
data_folder = '../Data'
log = pd.read_csv(os.path.join(data_folder, 'main_log.csv'), header=[0,1])
log#.head() # to see the whole table, comment out the .head()
# %% markdown
# ### Update the log
#
# - frame rate from RawImageInfo.txt
# - check the dropSize.xlsx for a, b, ID and OD
# - check traj.csv and xyz-traj.csv for 2D and 3D trajectory
# - check key visualization files
#     - 2D-image: "2d-traj.jpg"
#     - 3D-projection: "3d-traj-animation.avi"
#     - 3D-outRef: "3d-traj-RVRef.avi"
# %% codecell
img_folder = '/home/zhengyang/data/DE'

for num, i in log.iterrows():
    sf = os.path.join(img_folder, '{:08d}'.format(i[('params', 'Date')]), i[('params', 'Subfolder')])
    # RawImageInfo.txt
    imageInfo_dir = os.path.join(sf, 'RawImageInfo.txt')
    if os.path.exists(imageInfo_dir) == True:
        with open(imageInfo_dir, 'r') as f:
            fps = int(f.readline())
        log[('params', 'FPS')].at[num] = fps

    # dropSize.xlsx
    dropSize_dir = os.path.join(sf, 'dropSize.xlsx')
    if os.path.exists(dropSize_dir) == True:

        outer, inner, a, b = read_dropSize(dropSize_dir)
        log[('analysis', 'OD')].at[num] = outer
        log[('analysis', 'ID')].at[num] = inner
        log[('analysis', 'a')].at[num] = a
        log[('analysis', 'b')].at[num] = b

    # traj.csv
    traj_dir = os.path.join(sf, 'crop_HoughCircles', 'traj.csv')
    log[('analysis', '2D-trajectory')].at[num] = int(os.path.exists(traj_dir))
    # xyz-traj.csv
    xyz_dir = os.path.join(sf, 'crop_HoughCircles', 'xyz-traj.csv')
    log[('analysis', '3D-trajectory')].at[num] = int(os.path.exists(xyz_dir))
    # 2d-image.jpg
    image_2D_dir = os.path.join(sf, 'crop_HoughCircles', '2d-image.jpg')
    log[('Visual', '2D-image')].at[num] = int(os.path.exists(image_2D_dir))
    # 3d-traj-animation.avi
    projection_3D_dir = os.path.join(sf, 'crop_HoughCircles', '3d-traj-animation.avi')
    log[('Visual', '3D-projection')].at[num] = int(os.path.exists(projection_3D_dir))
    # 3d-traj-RVRef.avi
    outRef_3D_dir = os.path.join(sf, 'crop_HoughCircles', '3d-traj-RVRef.avi')
    log[('Visual', '3D-outRef')].at[num] = int(os.path.exists(outRef_3D_dir))
# %% codecell
log
# %% markdown
# ### Save the log
# %% codecell
log.to_csv(os.path.join(data_folder, 'main_log.csv'), index=False)
# %% markdown
# ### Add entries to log
# %% codecell
folder = '/home/zhengyang/data/DE/08122021'
l = readdata(folder, 'raw').sort_values(by='Dir')
for num, i in l.iterrows():
    print(os.path.relpath(os.path.split(i.Dir)[0], folder))
# copy to the csv spreadsheet
# %% markdown
# ## 2 Experiment overview
#
# Plot parameter distributions (histogram) to have a broad idea of what experiment is lacking.
# %% codecell
data_folder = '../Data'
log = pd.read_csv(os.path.join(data_folder, 'main_log.csv'), header=[0,1])
r = log[('analysis', 'OD')] / log[('analysis', 'ID')]
plt.figure()
r.hist(bins=3)
plt.ylabel("Histogram")
plt.xlabel("R/r")
plt.figure()
log[('analysis', 'ID')].hist(bins=3)
plt.xlabel('r')
plt.ylabel('Histogram')
# %% markdown
# ## 3 A Class for quickly accessing log entries
# %% codecell
class DE_log(pd.DataFrame):
    def __init__(self, log=log):
        '''log_data is a DataFrame containing the experiment log
        '''
        self.main_log = log
    def size_ratio(self, ratio_range):
        assert(len(ratio_range)==2)
        ratio = self.main_log[('params', 'OD')] / self.main_log[('params', 'ID')]
        return self.main_log.loc[(ratio>=ratio_range[0])&(ratio<ratio_range[1])]
# %% codecell
log = pd.read_csv(os.path.join('../Data', 'main_log.csv'), header=[0, 1])
# %% markdown
# ## 4 Structured log for XZ experiments
#
# After each day of experiment, the raw experiment log (written during experiments) will be reorganized into a structured log in .xlsx format. For XZ experiments, a typical structured log looks like the following:
# ![](img/structured_log_screenshot.png)
# %% markdown
# In this section, these logs are read and a statistics of the parameters are visualized.
# %% codecell
def read_structured_log_XZ(folder, append_date=True):
    """Read .xlsx files in given folder starting with `structured_log_` and concatenate them into a single table.
    Args:
    folder -- the folder containing the structured logs
    append_date -- add the experiment date as a column of the log. This is useful when trying to locate specific data
    Returns:
    df -- a single DataFrame of all logs
    Test:
    >>>folder = '/home/zhengyang/data/DE/Logs'
    >>>read_structured_log_XZ(folder, append_date=True)"""
    l = dirrec(folder, 'structured_log_*')
    df_list = []
    for Dir in l:
        df_temp = pd.read_excel(Dir)
        if append_date:
            date_str = os.path.splitext(os.path.split(Dir)[-1])[0].split('_')[-1]
            df_temp = df_temp.assign(date=date_str)
        df_list.append(df_temp)
    df = pd.concat(df_list)
    return df
# %% codecell
folder = '../Data/structured_log'
df = read_structured_log_XZ(folder, append_date=True)
# %% codecell
# mainly for filtering the anchor videos
df = df.loc[df['Plane']=='XZ']
df = df.loc[df['Quality']!='Bad']
# %% codecell
fig, ax = plt.subplots(figsize=(8, 2), dpi=150, nrows=1, ncols=4, sharey=True)
df['D'].hist(ax=ax[0])
df['D'].loc[df['Easy to analyze?']=='Yes'].hist(ax=ax[0])
df['d'].hist(ax=ax[1])
df['d'].loc[df['Easy to analyze?']=='Yes'].hist(ax=ax[1])
(df['D']-df['d']).hist(ax=ax[2])
(df['D']-df['d']).loc[df['Easy to analyze?']=='Yes'].hist(ax=ax[2])
(df['D']/df['d']).hist(ax=ax[3])
(df['D']/df['d']).loc[df['Easy to analyze?']=='Yes'].hist(ax=ax[3])
ax[0].set_xlabel('Outer diameter (um)')
ax[1].set_xlabel('Inner diameter (um)')
ax[2].set_xlabel('Difference (um)')
ax[3].set_xlabel('D/d')
ax[0].set_ylabel('Number of experiments')
# %% markdown
# Practically, it's easier to put data into fixed brackets and visualize the distribution of the parameters. In the XZ experiments, we have 3 major parameters: D, d and OD. Below I set a tentative bracket for all the parameters:
# ```
# OD_bracket = ((0, 25), (25, 50), (50, 75), (75, 100), (100, 125), (125, 150))
# D_bracket = ((0, 50), (50, 100), (100, 150), (150, 200))
# d_bracket = ((0, 20), (20, 40), (40, 60))
# ```
# OD will be considered as a parameter that is fixed for now (11/18/2021). We will examine the effect of D and d. Concentration effect will be addressed later when more data are available.
# %% codecell
# distribution of OD
fig, ax = plt.subplots(dpi=100)
df['OD'].hist(bins=range(0, 150, 25), ax=ax)
ax.set_xticks(range(0, 150, 25))
ax.set_xticklabels(range(0, 150, 25))
ax.set_yticks(range(0,21,5))
ax.set_yticklabels(range(0, 21, 5))
ax.set_xlabel('OD')
ax.set_ylabel('Number of experiments')
# %% codecell
# Take the middle column (50, 75), 26 experiment, to study the effect of D and d
nbins = 4 # number of bins
subdf = df.loc[(df['OD']>=50)&(df['OD']<75)]
fig, ax = plt.subplots(figsize=(8, 2), dpi=150, nrows=1, ncols=4, sharey=True)
subdf['D'].hist(ax=ax[0], bins=nbins)
# subdf['D'].loc[subdf['Easy to analyze?']=='Yes'].hist(ax=ax[0])
subdf['d'].hist(ax=ax[1], bins=nbins)
# subdf['d'].loc[subdf['Easy to analyze?']=='Yes'].hist(ax=ax[1])
(subdf['D']-subdf['d']).hist(ax=ax[2], bins=nbins)
# (df['D']-df['d']).loc[df['Easy to analyze?']=='Yes'].hist(ax=ax[2])
(subdf['D']/subdf['d']).hist(ax=ax[3], bins=nbins)
# (df['D']/df['d']).loc[df['Easy to analyze?']=='Yes'].hist(ax=ax[3])
ax[0].set_xlabel('Outer diameter (um)')
ax[1].set_xlabel('Inner diameter (um)')
ax[2].set_xlabel('Difference (um)')
ax[3].set_xlabel('D/d')
ax[0].set_ylabel('Number of experiments')
ax[0].set_yticks([0, 5, 10])
ax[0].set_yticklabels([0, 5, 10])
ax[0].set_xticks(np.linspace(subdf['D'].min(), subdf['D'].max(), 5))
ax[0].set_xticklabels(np.linspace(subdf['D'].min(), subdf['D'].max(), 5).astype('int'))
ax[1].set_xticks(np.linspace(subdf['d'].min(), subdf['d'].max(), 5))
ax[1].set_xticklabels(np.linspace(subdf['d'].min(), subdf['d'].max(), 5).astype('int'))
ax[2].set_xticks(np.linspace((subdf['D']-subdf['d']).min(), (subdf['D']-subdf['d']).max(), 5))
ax[2].set_xticklabels(np.linspace((subdf['D']-subdf['d']).min(), (subdf['D']-subdf['d']).max(), 5).astype('int'))
ax[3].set_xticks(np.linspace((subdf['D']/subdf['d']).min(), (subdf['D']/subdf['d']).max(), 5))
ax[3].set_xticklabels(np.linspace((subdf['D']/subdf['d']).min(), (subdf['D']/subdf['d']).max(), 5).astype('int'))
# %% codecell
subdf
# %% codecell
subdf.to_csv("OD50-75.csv")
# %% codecell
# copy data from raw folder to summary folder
# rename data file by adding date and number at the end
files_to_copy = ['traj_50.csv']
data_folder = '/media/zhengyang/NothingToSay/DE'
dest_folder = '../Data/Real_data'
unsuccessful_list = []
for num, i in subdf.iterrows():
    date_str = '{:08d}'.format(int(i.date))
    num_str = '{:02d}'.format(i['#'])
    for file in files_to_copy:
        file_dir = os.path.join(data_folder, date_str, 'Analysis', num_str, file)
        root, ext = os.path.splitext(file)
        if os.path.exists(file_dir):
            copy(file_dir, os.path.join(dest_folder, '{0}_{1}_{2}{3}'.format(root, date_str, num_str, ext)))
        else:
            unsuccessful_list.append(file_dir)
if len(unsuccessful_list) == 0:
    print("Data transfer complete.")
else:
    print("The following files are not successfully copied:")
    for item in unsuccessful_list:
        print(item)
