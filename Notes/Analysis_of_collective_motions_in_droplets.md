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



## III. Spatial and temporal correlation

We see collective motions in bulk and under confinement. Are they the same or different in any aspects? Let us try to understand this by looking at the spatial and temporal correlation functions.

## IV. 
