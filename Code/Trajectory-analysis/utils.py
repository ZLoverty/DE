import matplotlib.pyplot as plt
import numpy as np

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
    fig = plt.figure(figsize=(3, 3/img.shape[1]*img.shape[0]), dpi=200)
    ax = fig.add_axes([0,0,1,1])
    ax.imshow(img, cmap='gray')
    ax.axis('off')
    ax.scatter(traj.x, traj.y, s=0.7, c=np.arange(len(traj))/len(traj))
    plt.close()
    return fig