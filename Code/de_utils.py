import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter
from pivLib import read_piv
from skimage import io
from corrLib import divide_windows, readdata
import trackpy as tp
# %% codecell
def tangent_unit(point, center):
    """Compute tangent unit vector based on point coords and center coords.
    Args:
    point -- 2-tuple
    center -- 2-tuple
    Returns:
    tu -- tangent unit vector
    """
    point = np.array(point)
    # center = np.array(center)
    r = np.array((point[0] - center[0], point[1] - center[1]))
    # the following two lines set the initial value for the x of the tangent vector
    ind = np.logical_or(r[1] > 0, np.logical_and(r[1] == 0, r[0] > 0))
    x1 = np.ones(point.shape[1:])
    x1[ind] = -1
    y1 = np.zeros(point.shape[1:])
    x1[(r[1]==0)] = 0
    y1[(r[1]==0)&(r[0]>0)] = -1
    y1[(r[1]==0)&(r[0]<0)] = 1

    y1[r[1]!=0] = np.divide(x1 * r[0], r[1], where=r[1]!=0)[r[1]!=0]
    length = (x1**2 + y1**2) ** 0.5
    return np.divide(np.array([x1, y1]), length, out=np.zeros_like(np.array([x1, y1])), where=length!=0)

def intersection(lst1, lst2):
    """
    Return the intersection of two lists.
    """
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def fit_for_outer_drop_z(a, b, r, ri, traj):
    """
    Assume inner droplets are always sliding on the surface of outer droplets.
    Find the z position with the least net deviation of trajectories from the surface.

    Args:
    a -- x coordinate of outer drop center
    b -- y coordinate of outer drop center
    r -- outer drop radius
    ri -- inner drop radius
    traj -- xyz-traj.csv DataFrame

    Returns:
    c -- z coordinate of outer drop center
    """
    err = 1e9
    for c_temp in np.linspace(0, r): # this assumes the real center lies in(0, r)
        dx = traj.x - a; dy = traj.y - b; dz = traj.z - c_temp
        temp_err = (((dx**2 + dy**2 + dz**2)**0.5 - (r-ri))**2).sum()
        plt.scatter(c_temp, temp_err)
        if err > temp_err:
            err = temp_err
            c = c_temp
    plt.scatter(c, err, s=100, marker='x', c='red')

    return float(c)

def plot_traj_overlay(traj, img):
    """Plot particle trajectory on the initial frame of an image sequence
    This function visualize the strength of fluctuation relative to the confinement size

    Args:
    traj -- DataFrame comprising columns x and y
    img -- an array like image

    Returns:
    fig -- the figure object
    """
    fig = plt.figure(figsize=(3, 3/img.shape[1]*img.shape[0]), dpi=300)
    ax = fig.add_axes([0,0,1,1])
    ax.imshow(img, cmap='gray')
    ax.axis('off')
    ax.scatter(traj.x, traj.y, s=0.7, c=np.arange(len(traj))/len(traj))
    plt.close()
    return fig

def center_traj(log_entry, folder):
    '''load trajectory and shift trajectory to a coordinate system with origin at the top of outer droplet
    This function assumes inner droplets are always sliding on the outer surfaces.
    Z positions are calculated based on xy positions.'''
    R = log_entry[('analysis', 'OD')] / 2
    r = log_entry[('analysis', 'ID')] / 2
    a = log_entry[('analysis', 'a')]
    b = log_entry[('analysis', 'b')]
    traj = load_xyz_traj(log_entry, folder)
    traj['x'] = traj['x'] - a
    traj['y'] = traj['y'] - b
    traj['z'] = R - r - ((R-r)**2 - traj['x']**2 - traj['y']**2) ** 0.5
    return traj

def r3(x, a):
    return a * x ** 3

def load_xyz_traj(log_entry, folder):
    '''Use log entry to load trajectory data from xyz-traj.csv'''
    date = '{:08d}'.format(log_entry[('params', 'Date')])
    subfolder = log_entry[('params', 'Subfolder')]
    traj_dir = os.path.join(folder, date, subfolder, 'crop_HoughCircles', 'xyz-traj.csv')
    if os.path.exists(traj_dir):
        return pd.read_csv(traj_dir)
    else:
        print('Data not found')

# %% codecell

# %% codecell


# %% codecell
if __name__=="__main__":
