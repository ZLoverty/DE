---
layout: "post"
title: "model discussion summary "
date: "2022-02-25 11:31"
---

### Stochastic model discussion summary

##### Formulation and solution

We will continue the discussion with the equations and solutions given by Maggi 2014:

$$
\dot y = -\mu ky + \eta^T + \eta^A,
$$

where $\eta^A$ is the active noise, satisfying $\left< \eta^A(t)\eta^A(t') \right>=(D_A/\tau)e^{-|t-t'|/\tau}$. The active part of the solution is

$$
\left< \Delta y^2(t) \right> = \frac{2D_A}{\mu k} \frac{1-e^{-\mu kt} - \mu k\tau(1-e^{-t/\tau})}{1-(\mu k\tau)^2}.
$$

We let $\mu k = 1/\tau^*$, and it can be shown that the $\tau^*$ here is the saturation time scale of inner droplet motion.

##### Limit cases

$$
t\to 0:\, \left< \Delta y^2(t) \right> = \frac{D_A}{\tau(1+\tau/\tau^*)} t^2
$$

$$
\tau^*\gg t\gg \tau:\, \left< \Delta y^2(t) \right> = \frac{2D_A}{1-(\tau/\tau^*)^2}(t-\tau)
$$

$$
t\to\infty:\, \left< \Delta y^2(t) \right> = \frac{2D_A\tau^*}{1+\tau/\tau^*}
$$

##### Evaluate $R_\infty$ and $\tau^*$

A typical MSD curve can be described by the saturation value $R_\infty^2$ and the transition time $\tau^*$. The ballistic regime, where $\left< \Delta y^2(t) \right> \propto t^2$, is usually within 1 second and is difficult to measure accurately in experiment.

![illustrate sat value and transition time](../images/2022/02/illustrate-sat-value-and-transition-time.png)

The transition time $\tau^*$ comes out directly from the model as

$$
\tau^* = \frac{1}{\mu k},
$$

where $\mu=(6\pi\eta r_i)^{-1}$ is the particle mobility and $k=m^*g/(r_o-r_i)$ is the effective spring constant.
Notice that $m^*$ is the buoyant mass of the oil droplet in water, and can be computed as $m^*=\Delta\rho\frac{4}{3}\pi r_i^3$. Taken together, $\tau^*$ can be expressed as

$$
\tau^* = \frac{9\eta}{2\Delta\rho g}\frac{r_o-r_i}{r_i^2} =  \frac{9\eta}{\Delta\rho g}\frac{D-d}{d^2}
$$

In the limit $\tau^*\gg\tau$, the saturation value $R_\infty^2\approx 2D_A\tau^*\propto\tau^*\propto (D-d)/d^2$,

$$
R_\infty \propto \frac{\sqrt{D-d}}{d}.
$$

When $\tau^*\sim\tau$, the experimental determination of $\tau^*$ becomes problematic.

##### Experimental data

The current data set presents 3 parameters: $D, d, n$ and two observables: $R_\infty$ and $\tau^*$. $D$ and $d$ are always combined as $(D-d)/d^2$ as $x$-axis. Bacterial concentration $n$ is encoded using `tab10` colormap, with the following mapping.

![bacterial concentration colormap](../images/2022/02/bacterial-concentration-colormap.png)

The data here combines Chile and Paris data. To discern them, I use solid circle to plot Paris data, and empty triangle to plot Chile data.

Parameter distribution:

![parameter distribution](../images/2022/02/parameter-distribution.png)

$\tau^*$ vs. $(D-d)/d^2$

![tau star](../images/2022/02/tau-star.png)

$R_\infty$ vs. $(D-d)/d^2$

![Rinf](../images/2022/02/rinf.png)

##### Some attempts

Rescale $R_\infty$ with $n$ (OD)

![rescale Rinf with OD](../images/2022/02/rescale-rinf-with-od.png)

Plot $R_\infty^2 / \tau^*$ vs. $(D-d)/d^2$ ($=\frac{2D_A}{1+\tau/\tau^*}$)

![rinf2 tau star 1](../images/2022/02/rinf2-tau-star-1.png)

Plot $R_\infty^2$ vs. $\tau^*$ (similar to above, expect a linear regime)

![rinf2 vs tau star](../images/2022/02/rinf2-vs-tau-star.png)

Separate $(D-d)/d^2$ regimes (already evidenced in $R_\infty^2 / \tau^*$ vs. $(D-d)/d^2$ plot)
