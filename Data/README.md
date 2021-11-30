# Data
This folder contains files that describe the data of this project.
The ~actual data~ full data set (in particular images) are saved locally in an external hard drive, and can be retrieved by the info in these files.

The structure of this folder is
```
Data
|- structured_log
  |- structured_log_mmdd(date).xlsx
  |- ...
|- Real_data
  |- traj_50_...
  |- MSD_50_...
|- exp_log.txt (general information of what is done/tested)
|- Archive (not maintained from 08132021, legacy of the project)
  |- DE Size Control-Data.csv (flow rates and droplet sizes (for a specific device which is broken now. So the exact values in this data may not be useful any more)
  |- main_log.csv
```
**NOTE:** this folder only has text and binary data. No graphs!

## Maintainence
### Daily
- **exp_log.txt:** Each day after experiment, an entry should be added in `exp_log.txt`, with a date and a general discription of what is tested in the day. This could be a combination of the general log and contents of hand-written logs.
- **structured_log:** Each day after experiment, rewrite the unstructured log into structured log.  

## Contents
### Real_Data
Store light weight data here. A comprehensive list of data type is [traj_50, MSD_50]. ~In the future, when frame-by-frame tracking is possible, we can add [traj, MSD, VACF, ...].~

For each data type, we create a folder and put files corresponds to different experiment into the same folder. Since I used to these files the same and put them in different folders, doing this requires renaming every file. The rename scheme is the following: **after the original file name, add `_date_subname`**. For example, `traj_50.csv` from 11022021/01 will be renamed to `traj_50_11022021_01.csv`
### structured_log
This folder contains experiment logs organized in excel sheets.
The formats are designed for double emulsions in both XY and XZ plane.
More variables from experiments are hosted in `comments` and will be considered in the future.  

