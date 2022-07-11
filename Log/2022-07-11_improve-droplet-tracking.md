---
layout: "post"
title: "improve droplet tracking"
date: "2022-07-11 10:21"
---

### Improve droplet tracking

At the beginning, I tried HoughCircles algorithm (HC) to detect inner droplets. If the droplet is large and has sharp dark boundary, HC works well. However, if the droplet is small, many false detections come up and make the results very "dirty".

Then, I got an idea that I can perform HC on cropped regions. The idea is to use the droplet position in frame 1 to crop frame 2, then use HC on the cropped region to find droplets. I call this method _crop HoughCircles_ (cHC). This method can significantly reduce the number of false detections. However, if it makes mistakes in the process, it will likely lead the cropped region to a wrong place, making subsequent detections difficult. This method is therefore not robust.

Since the failure of cHC, I started to use the most primitive method - hand tracking - to get droplet trajectories. In a typical video, I have 30,000 frames. It is very challenging to do hand tracking on so many frames, so I only do it every 50 frames (corresponding to 1 s). In this way, I got the first trajectory data set, of which the temporal resolution was 1 s. This resolution allows me to measure the relaxation time scale and the saturation value of MSD, but measuring the ballistic regime remains impossible.

![first data set](../images/2022/07/first-data-set.png)

Recently, I obtained a new data set of lower bacterial concentration. Since the motion is in general weaker, I start to think that I can get better results with HC. This time, after carefully reading the document of HC, I find two important parameters that can improve the tracking: `param1` and `param2`.

>**param1**	First method-specific parameter. In case of HOUGH_GRADIENT and HOUGH_GRADIENT_ALT, it is the higher threshold of the two passed to the Canny edge detector (the lower one is twice smaller). Note that HOUGH_GRADIENT_ALT uses Scharr algorithm to compute image derivatives, so the threshold value shough normally be higher, such as 300 or normally exposed and contrasty images.
>
>**param2**	Second method-specific parameter. In case of HOUGH_GRADIENT, it is the accumulator threshold for the circle centers at the detection stage. The smaller it is, the more false circles may be detected. Circles, corresponding to the larger accumulator values, will be returned first. In the case of HOUGH_GRADIENT_ALT algorithm, this is the circle "perfectness" measure. The closer it to 1, the better shaped circles algorithm selects. In most cases 0.9 should be fine. If you want get better detection of small circles, you may decrease it to 0.85, 0.8 or even less. But then also try to limit the search range [minRadius, maxRadius] to avoid many false circles.

Adjusting these two parameters can always lead to a satisfactory degree of false positive cases, while keeping the correct detection. With these two parameters adjusted, I don't have to use cHC to avoid false positive. So even if the algorithm makes mistakes in the process, the mistake will not lead to more mistakes in the next frames, making the method robust. With this method, I'm able to obtain some full trajectories.

![full trajs](../images/2022/07/full-trajs.png)

##### Problems of HC algorithm

The python implementation of HC ([cv.HoughCircles()](https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d)) has two main issues:

- No subpixel accuracy: all the detections are separated from each other by integer pixels.

![subpixel accuracy](../images/2022/07/subpixel-accuracy.png)

- Inconsistent detection: whether it detects the inner edge or the outer edge of a droplet is not consistent, because it only considers the pixel intensity gradient.

![inconsistent detection](../images/2022/07/inconsistent-detection.png)

In the Matlab `imfindcircle()` function, the subpixel accuracy issue is handled. I'm not sure if the inconsistent detection issue is also handled or not.

Here, I'm going to add a correction step to make the trajectory more accurate.

##### Correction of HC results

All the droplets in images have dark edges, which may be a result of strong refraction at the edges. If we draw a line from droplet center, in the radial direction, to outside the droplet, the image intensity profile along that line would likely show a valley (a dark peak). This valley is a more unambiguous indicator of the droplet position. By drawing multiple (>3) lines and fit each to get a valley position, we get the coordinates of multiple points on the droplet, from which we can fit a circle.

![cross boundary intensity](../images/2022/07/cross-boundary-intensity.png)

As the first implementation, I sample four points from top, bottom, left and right to fit circle. Then, for better statistics and accuracy, I take more samples from various directions. However, that leads to a problem, where the outer droplet boundaries are included in the profile and make the valley detection wrong. To fix this, I set a angular range, and only use intensity profiles in that range to fit for valleys. As an example, I show in the right panel of the figure above, where I only find valleys on the left of the inner droplet. The valley detection turns out to be much better than in the middle panel.

##### Tracking quality

This correction can clearly improve the tracking in most images. But in some images, the results are still not ideal and can be improved. It is desired to have a number to quantify the tracking quality, so that we can easily identify which tracking can be improved.

![tracking quality](../images/2022/07/tracking-quality.png)

On the left, I plot the original and the corrected droplet position. On the right, I plot the pixel intensity profiles along the two contours. As can be seen, the original intensity profile shows stronger fluctuations than the corrected one. Hence, we can use the standard deviation of the contour intensity profile to quantify the tracking quality. The larger the standard deviation, the worse the tracking quality.

For the two profiles in the image for example,
$$
\sigma_o = 40.8,\, \sigma_c = 23.6
$$
To make the number more intuitive, we rescale the value with image pixel standard deviation, and the substract from 1, so that the maximum becomes 1, and the value typically ranges from -1 to 1. We define this as _tracking quantity Q_:
$$
Q = 1 - \frac{\sigma_{\text{ctr}}}{\sigma_{\text{img}}}
$$
with $\sigma_{\text{img}}=35.6$, we can compute the tracking quality before and after the correction:
$$
Q_o = -0.15,\, Q_c = 0.34
$$
Clearly, the corrected circle has a better quality since $Q_c>Q_o$.

##### Processing large image sequence

As I noted before, a typical video consists of 30,000 frames. So far, it is challenging to make all the correction great using the same parameter. For example, I show below the tracking quality time series of both original and corrected tracking:

![tracking quality ts](../images/2022/07/tracking-quality-ts.png)

There are strong fluctuations in both original and corrected trajectories. In particular, there are multiple instances where the corrected tracking has $Q<0$. Let's see what happens there, for example in frame 40, we have

![bad correction](../images/2022/07/bad-correction.png)

We can see that it's just because the upper right cross boundary line touches the outer droplet edge, leading to one point that is not really on the inner droplet edge. And that leads to a big deviation from the correct fitting. To avoid this, I add another input argument `sample_range`, so that I can specify the angle range within which I extract intensity profiles. This is noted before, and with this modification, I'm able to improve the tracking quality on this image.

![good correction](../images/2022/07/good-correction.png)

To quantify the tracking quality of the whole image, we can count the number of frames where the tracking quality decreases after correction. Let's use the same image sequence for example, we get 13.8% of frames getting worse after correction for the method without `sample_range`. And by searching only in the left side, I can improve the getting worse rate to 2.9%. The tracking quality time series of the original, initial correction and the refined correction are shown below:

![quality ts](../images/2022/07/quality-ts.png)

##### Circle fitting

Circle fitting turns out to be an important technique in this correction. I used to apply a gradient descent algorithm to find an optimization with the least square error from data points to fitted circle edge. Formally, the optimization tries to find $a$, $b$ and $r$ that minimize the residual
$$
f(a, b, r) = \sum_{i=1}^{n} [(x_i-a)^2+(y_i-b)^2 - \bar r^2]
$$
where $\bar r = \frac{1}{n}\sum_{i=1}^{n}\sqrt{(x_i-a)^2+(y_i-b)^2}$.
