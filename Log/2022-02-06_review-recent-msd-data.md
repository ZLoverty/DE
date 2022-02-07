---
layout: "post"
title: "review recent msd data"
date: "2022-02-06 09:42"
---

### Review recent msd data

Cristian and I obtained more inner droplet motion data during his intern in Paris. In this note, I review these data and pick out the useful ones.

![od dist recent msd](../images/2022/02/od-dist-recent-msd.png)

##### 50-70 contains 29 experiments, and is the densest bin with size 20

With in this OD bracket, the outer and inner droplet diameters has the following distribution:

![diameter dist 50 70](../images/2022/02/diameter-dist-50-70.png)

![d dist 50 70](../images/2022/02/d-dist-50-70.png)

##### First, plot 5 MSD on one plot and manually measure $R^\infty$ and $\tau^*$, meantime filter out too short or too jumpy trajectories.


![MSD recent 50 70 man](../images/2022/02/MSD_recent_50_70_man.svg)

##### Plot all the MSD's in the same plot, try to rescale $\left< \Delta y^2 \right>$ with $(D-d)^2$. (unsuccessful attempt)

![all together msd](../images/2022/02/all-together-msd.png)

rescale y-axis

![msd rescale](../images/2022/02/msd-rescale.png)

##### It's also interesting to rescale  $\left< \Delta y^2 \right>$ in such a way that all the plateau values collapse, to inspect the time scale difference.

![rescale msd with Rinf](../images/2022/02/rescale-msd-with-rinf.png)


##### If we rescale $\Delta t$ with $\tau^*$ as well, all the curves can be collapsed.

![collapse all msd curves xy](../images/2022/02/collapse-all-msd-curves-xy.png)

Such collapse demonstrates that the motions of inner droplets share a similar pattern, which can be described by two parameters $R^\infty$ and $\tau^*$. However, theoretical understanding of these two parameters, in particular how confinement influences them, is still lacking.

##### Next, we try to reveal the confinement effect by plotting $R^\infty$ and $\tau^*$ as functions of $D$ and $d$.

vs. D

![RtD](../images/2022/02/rtd.png)

vs. d

![Rtddd](../images/2022/02/rtddd.png)

vs. D/d

![RtDd](../images/2022/02/rtdd.png)
