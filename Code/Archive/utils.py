from corrLib import readdata
import pandas as pd
import numpy as np

def search_key_files(folder, key_ext='raw'):
    """
    Search for the key files, return the date and relative directory of the files, as DataFrame.
    
    Args:
    folder -- main folder to search
    key_ext -- file name extension of the key files to be searched 
                default 'raw' is the raw image extension by bacteria.vi
                
    Returns:
    dir_list -- (date, relative_dir) DataFrame
    """
    
    date_list = []
    sf_list = []
    l = readdata(data_folder, 'raw')
    for num, i in l.iterrows():
        rdir = os.path.relpath(i.Dir, folder)
        rdir_folder = os.path.split(rdir)[0]
        date, sf = rdir_folder.split('/', 1)
        date_list.append(date)
        sf_list.append(sf)
    
    dir_list = pd.DataFrame({'Date': date_list, 'Subfolder': sf_list}).sort_values(by=['Date', 'Subfolder'])
    
    return dir_list


def read_dropSize(dropSize_dir):
    """
    Read dropSize.xlsx file for inner and outer droplet sizes.
    
    Args:
    dropSize_dir -- absolute directory of dropSize.xlsx
    
    Returns:
    outer, inner -- outer and inner droplet sizes (um), rounded to 1 decimal place (numbers in row 5)
    """
    
    s = pd.read_excel(io=dropSize_dir)
    outer = np.around(s['outer'][5], 1)
    inner = np.around(s['inner'][5], 1)
    a = np.around(s['a'][5], 1)
    b = np.around(s['b'][5], 1)
    
    return outer, inner, a, b