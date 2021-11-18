import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

def msd_to_velocity(msd):
    """This function fit the ballistic regime of MSD to calculate velocity
    <dr^2>=(vt)^2
    Args:
    msd -- a pandas Series with lagt as index and msd as data
            or a pandas DataFrame with lagt as index and column name as msd
    Returns:
    v -- velocity of fitting (unit is consistent with the input data)"""
    if isinstance(msd, pd.Series):
        msd = msd.to_frame('msd')
    assert(isinstance(msd, pd.DataFrame))
    assert('msd' in msd)
    def lin_1(x, b):
        return x + b
    
    x = np.log(msd.index)
    y = 0.5 * np.log(msd['msd'])
    popt, pcov = curve_fit(lin_1, x, y)
    v = np.exp(popt[0])
    
    return v