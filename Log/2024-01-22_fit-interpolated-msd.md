---
date: 2024-01-22
title: fit interpolated msd 
author: Zhengyang Liu
---
# Fit interpolated MSD

## 1. LOG Y - the old method
We are trying to find the best way to fit our MSD data, hoping that we can extract the most reasonable parameters from the fitting. Our MSD data consist of a time series and a displacement series. The time data are typically evenly spaced in linear scale. Both time and displacement data span multiple orders of magnitude. Due to the large span, the fitting residual at higher magnitude is usually too large so that the residual at lower magnitude plays no role in the fitting result. To give lower magnitude data more weight, we come up with the idea that we take the logarithmic of the displacement data, bringing them to the same magnitude, and then fit. Formally, say we have a model

$$
\left<\Delta r^2\right> = f(\Delta t),
$$

where $\left<\Delta r^2\right>$ and $\Delta t$ are the displacement and time data, what we actually fit is 

$$
y = \log \left<\Delta r^2\right> = g(\Delta t).
$$

Recently, we realize that this method still has a weight related drawback. That is, while we are trying to capture the curve in log-log space, we are fitting the data that are evenly spaced in linear scale. It is apparent that such data won't be evenly spaced in log space. Instead, the data points are sparser at small scale, and are denser at large scale. As a result, we are still putting more weight to the large scale with this method. 

## 2. INTERP - the new method

To fix this issue, we interpolate the MSD data to make time data evenly spaced in log space. This way, we have the same weight in the log scale, so we can capture the short time regime better. An example of such interpolation is shown below. The blue dots are the raw data points, and the gray circles are the interpolated points.

![picture 0](/assets/images/2024/01/interpolation-example.png)  

We then fit the interpolated data with the LOGY model. The fitting results for the above data is shown below, where the red curve and blue curve represents the fitting on raw data and interpolated data, respectively. The two curves are hardly distinguishable, but we notice that the blue curve captures the small scale data better.

![picture 1](/assets/images/2024/01/fit-results.jpg)  

## 3. Compare the results 

Now taht we have the new method, it is interesting to compare the fitting results of both methods. The comparison is shown in the plots below. Gray points are from the old method, while the blue points are from the new method. For $\tau$, we again observe no dependence on $r_i$. $D_A$ seems to show an weak increasing trend on $r_i$. And $\tau^*$, as previously observed and theoretically derived, shows and increasing trend on $(r_o-r_i)/r_i^2$.

![picture 2](/assets/images/2024/01/compare-results.png)  
