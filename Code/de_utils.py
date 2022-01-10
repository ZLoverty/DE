import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter
from pivLib import read_piv
from skimage import io
from corrLib import divide_windows, readdata

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
