# Analysis of Collective Motions in Droplets

In this note, I summarize the analysis on the collective motions of bacteria in droplets. Most analysis will be performed on the PIV data. More ambitiously, I can try to compare PIV analysis with the optical flow methods in Hamby2018.

## I. Masked PIV

The need for masked PIV arises from the study of bacterial flow field in droplets. Unlike previous bulk experiments, where the whole field of view is filled with bacteria, the images I have now usually have all bacteria confined in parts of the images. The followings are typical images I obtained recently, with one or more droplets in each image.

![typical droplet images](img/PIV_mask_required.png)

The first image is a bright field image of a double emulsion in the XZ plane (gravity pointing to the left). The boundary is not very clean so that the left boundary of the droplet does not show completely. The second image is a confocal image of several small droplets. The third image is a bright field with a cleaner boundary, so that even the left edge can be seen clearly. The fourth droplet is the confocal image of the same droplet in the third image.

### A. Masking method

#### 1. Rectangle + circle
Initially, I came up with a two-step masking scheme to deal with images like the first image. Specifically, step one is to apply a rectangular region of interest bonding the droplet (red rectangle); step two is to specify the center position and radius of the droplet (yellow circle). This scheme is illustrated in the following sketch.

![ROI procedure](img/piv_drop.png)

Following this masking procedure, PIV analysis is performed in the rectangular ROI, and only the velocities inside the yellow circle are kept as valid velocities.

#### 2. Flexible mask

This rectangle + circle masking works well for single droplet images. However, for images containing multiple droplets, or more complicated morphological features, more flexible masks are required. For example, rectangle + circle is not sufficient for masking the second image, where multiple droplets present. In this scenario, I can manually draw a **mask image** in ImageJ based on the raw image, and pass this image to PIV algorithm as a mask. Below is the second image and its corresponding mask, as an example.

![mask2](img/mask2.svg)

This mask can then be used with the function `PIV_masked()` in `pivLib`, by passing the mask image as an argument. As an example, we test `PIV_masked()` on above left image (image 2), with the right image as the mask image, by running
```python
x, y, u, v = PIV_masked(I20, I21, 20, 10, 0.02, mask2)
```
As can be seen in the result below, yellow PIV arrows are found in both big droplets. The small droplet is smaller than the PIV box size, so no velocity is detected there.

![flex mask](img/flex_mask_piv.jpg)

### B. Masking procedure

There are several ways to use the mask. To mask the raw images before applying PIV or to mask the final velocity result, or to do both. How much do these options affect the final result of the PIV analysis? We test the following procedures:

1. Mask raw images by setting background 0, then apply PIV.
2. Apply PIV directly on raw images, then apply mask on velocity.
3. Mask raw images by setting background nan, then apply PIV. (PIV algorithm does not support nan pixels for the moment, so this cannot be tested yet).

The test code can be found in `Masked_PIV.py`. Use Hydrogen to view the results by `Run all`.

Results:
- Procedures 1 and 2 gives very similar results.
- Procedure 1 runs a little bit faster, so we implement `PIV_masked()` function with it.

Below are some plots comparing the overall velocity field, velocity PDF and running speed:

- overall velocity

![overall velocity](../images/2021/12/overall-velocity.png)

- velocity PDF

![velocity pdf](../images/2021/12/velocity-pdf.png)

- running speed

![running speed](../images/2021/12/running-speed.png)

## II. Does bacterial activity decays over time?

We know that after a couple of hours, most bacteria in droplets stop moving and droplets look like "frozen". But, is there a more **precise time scale** for this "freezing" process? What is the **major cause** of this phenomenon? Here we examine **bacterial activity over time** in several different droplets and try to estimate this time scale.

### A. Experiment

My experiment comprises **4 10-minute videos of the same droplet** whose diameter is 55 um (snapshots can be found in the following figure 21-24). 21 and 23 are bright field images, 22 and 24 are confocal images. Images were taken in order from 21 to 24, and the time delay between two videos was less than one minute and should be _negligible_.
19-20 are also bright field and confocal images of the same droplet with smaller size. The size of the droplet is comparable to PIV box size and may detoriote the PIV quality. Therefore, we only use 21-24 for the analysis.

![](img/19-24.svg)

### B. Results and discussion

Below is the mean velocity of PIV velocities in videos 21-24.

![mean velocity evolution](../images/2022/01/velocity_in_droplet.svg)

We note a few things from this measurement:
1. **velocity decay is most pronounced in the first 10 min**, later on the velocity remains constant for 30 min
2. Confocal measures a **higher** mean velocity
3. Confocal laser **does not** seem to harm bacterial activity
4. the **sudden drop of velocity** in the middle of yellow curve is not expected, watch video to find out why.

## III. Order parameter

### A. Order parameter in literatures
> 1. Wioland, H., Woodhouse, F. G., Dunkel, J., Kessler, J. O. & Goldstein, R. E. Confinement Stabilizes a Bacterial Suspension into a Spiral Vortex. Phys. Rev. Lett. 110, 268102 (2013).
>
> ![wioland2013](../images/2022/01/wioland2013.png)

### B. Compute order parameter from my PIV data
#### 1. Compute tangent unit vecotr field
To compute the order parameter above, we first need to compute the tangent unit vector $t_i$. Let $x$, $y$ be the point of interest, $x_1$, $y_1$ be the tangent unit vector, we know that $x_1$ and $y_1$ should satisfy
$$
xx_1 + yy_1 = 0 \\
x_1^2 + y_1^2 = 1
$$
We can set $x_1$ arbitrarily and $y_1$ can be calculated. Then $x_1$ and $y_1$ can be rescaled to meet the unit vector requirement. For example, we have $(x, y)=(1, 1)$. Set $x_1=1$, we get $y_1=-1$. Then rescale $x_1$ and $y_1$ by the length of $(x_1, y_1)$, $l=\sqrt{x_1^2+y_1^2}$ to get the unit vector. This is illustrated in the following figure.

![example tu](../images/2022/01/example-tu.png)

Here I notice that it's important to set the sign of $x_1$. For example, if we set $x_1=-1$ in the first place, the arrow in the above figure would be in the opposite direction (the red arrow). If we set all $x_1$'s to $-1$ for example, we end up with a vector field like the following, which is not coherent and is clearly wrong.

![all -1 vectors](../images/2022/01/all-1-vectors.png)

To make the arrow direction coherent through out the whole droplet, roughly speaking, we need to set half of the $x_1$'s positive and the rest negative. In my code, this is taken care of by the following lines:
```python
ind = np.logical_or(r[1] > 0, np.logical_and(r[1] == 0, r[0] < 0))
x1 = -1 * np.ones(len(point[0]))
x1[ind] = 1
```
**numpy logical functions** help determines the signs of each $x_1$ in batch. With this modification, we get the correct vector field.

![correct tangent vectors](../images/2022/01/correct-tangent-vectors.png)

On a mesh grid (like PIV data), the tangent unit vector field is the following

![meshgrid tu](../images/2022/01/meshgrid-tu.png)

#### 2. Compute order parameter from PIV data

> **An aside**
>
> When I plot the tangent unit vectors on top of an image, they no longer look like circulation, but rather and extension flow.
>
> ![error coords tu](../images/2022/01/error-coords-tu.png)
>
> Red is the tangent unit vector we just computed. Yellow arrows are the PIV data. **This is clearly an error caused by coordinates inconsistency**.
> To understand this inconsistency, see the sketch of coordinate systems below
>
> ![ordinary and image coordinates](../images/2022/01/ordinary-and-image-coordinates.png)
> The conversion between these two systems is not a simple rotation, but consists a mirror reflection. This makes the $x_1$ initiation rule opposite.
> ```python
> ind = np.logical_or(r[1] > 0, np.logical_and(r[1] == 0, r[0] > 0))
> x1 = np.ones(point.shape[1:])
> x1[ind] = -1
> ```

With the change in tangent unit vector field computation, we can now examine the circulating flow inside droplets.

![compare velocity with azimuthal](../images/2022/01/compare-velocity-with-azimuthal.png)

Using the formula given in III.A, we get an order parameter for the PIV data in the example $\phi=0.23$. According to Wioland 2013, $\phi>0$ indicates the **existence of a coherent circulation**.

The whole video No.22 shows noisy order parameter oscillation between -0.4 and 0.4. The positivity is not pronounced compared to the noise.

![order parameter 22](../images/2022/01/order-parameter-22.png)

<font color="red">But note that this order parameter does not reflect any information about the oscillatory motion. By taking the absolute value of $v_i \cdot t_i$, no matter $v_i$ is parallel or antiparallel to $t_i$, the outcome is the same. </font>

## IV. Validity of PIV analysis

### A. Visual inspection

**So far the best way to validify PIV analysis is visual inspection.** Such inspection is two-fold. First, we can compare hand measured velocity with PIV results quantitatively. This can be done for a few frames, and doing it for all the data is unfeasible. _Actually, that's why we use PIV, because it's more efficient with large data set._ Second, we can plot PIV arrows on top of corresponding images and see roughly if the directions and magnitude make sense.


#### 2. Make overlay movies
**A python function `matplotlib.pyplot.quiver(...)` is used to plot the velocity field of PIV.** By default, `quiver` automatically determines a proper scale for each velocity field. This is kind of similar to the contrast autoscaling for images, which makes sure that an image is not too dark or too bright, and patterns can be seen. While autoscaling is always good for a single image, for a video with many frames it's better to fix the scale, because a direct feeling of relative magnitude is important in a dynamic process. For example, if we fix the light intensity scale, we will know if the overall light intensity changes from one frame to another. **`quiver` provides a "complicated" method to control the scale, by combining keywords `scale` and `scale_units`.** `scale` is the number of data units per arrow length unit, e.g., m/s per plot width. `scale_units` is the arrow length unit, and can be `{'width', 'height', 'dots', 'inches', 'x', 'y', 'xy'}`. See the [official document of `quiver`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.quiver.html) for more detailed information. **In the `piv_overlay.py` script, we have access to the PIV data information and the output image information.** We know the how many arrows we are going to plot, on what height and width. We want the arrows to be large so that we can see them clearly. We also don't want to make them too large to block other arrows. A good choice of maximum arrow length is the PIV box size, i.e. width / ncol. **To set this, we let `scale_units='width'`, and let `scale=max(u.max(), v.max())*ncol`.** The interpretation of this setting is: the largest velocity component has length of width / (number of columns). Note that this only needs to be set once for an image sequence. From the second PIV data, we use constant `scale`.

#### 1. Make overlay movies
**A python function `matplotlib.pyplot.quiver(...)` is used to plot the velocity field of PIV.** By default, `quiver` automatically determines a proper scale for each velocity field. This is kind of similar to the contrast autoscaling for images, which makes sure that an image is not too dark or too bright, and patterns can be seen. While autoscaling is always good for a single image, for a video with many frames it's better to fix the scale, because a direct feeling of relative magnitude is important in a dynamic process. For example, if we fix the light intensity scale, we will know if the overall light intensity changes from one frame to another. **`quiver` provides a "complicated" method to control the scale, by combining keywords `scale` and `scale_units`.** `scale` is the number of data units per arrow length unit, e.g., m/s per plot width. `scale_units` is the arrow length unit, and can be `{'width', 'height', 'dots', 'inches', 'x', 'y', 'xy'}`. See the [official document of `quiver`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.quiver.html) for more detailed information. **In the `piv_overlay.py` script, we have access to the PIV data information and the output image information.** We know the how many arrows we are going to plot, on what height and width. We want the arrows to be large so that we can see them clearly. We also don't want to make them too large to block other arrows. A good choice of maximum arrow length is the PIV box size, i.e. width / ncol. **To set this, we let `scale_units='width'`, and let `scale=max(u.max(), v.max())*ncol`.** The interpretation of this setting is: the largest velocity component has length of width / (number of columns). Note that this only needs to be set once for an image sequence. From the second PIV data, we use constant `scale`.

**Qualitatively, the arrows point to the same direction as the motions.** <font color='red'> Link to piv overlay of 22 </font> The reason why the mean velocity is small could be that the velocity in the interior of droplets are in general small. The following animation is a pair of adjacent frames sampled from my data. On the right is the velocity field from PIV analysis.

![piv gif](../images/2022/01/piv_gif.gif) ![piv](../images/2022/01/00050.jpg)

#### 2. Manually measure velocity

**Quantitatively,**

### B. Window size effect
### C. PIV on bacteria directly: is this a justified method?

**Using bacteria directly as tracer particles for PIV is still not well accepted by the community**, according to my experience with the previous two papers (Science Advances 2021 and Soft Matter 2021).
## IV. Spatial and temporal correlation

We see collective motions in bulk and under confinement. Are they the same or different in any aspects? Let us try to understand this by looking at the spatial and temporal correlation functions.











# Appendix A
To do list
- For high bacterial concentration: Compare flow time scale with inner droplet motion time scale
- For low bacterial concentration: need a "zero control", a double emulsion without bacteria
- Should I include one more ring near the droplet edge?
