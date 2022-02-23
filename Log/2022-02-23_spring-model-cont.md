---
layout: "post"
title: "spring model cont"
date: "2022-02-23 08:43"
---

### Spring model - continue discussion

During the discussion with Eric, he pointed out that our solution to the stochastic equation does not recover the 0-memory limit when setting $\tau\to0$ (or $\nu\to\infty$). The solution given by Maggi 2014, however, does not have this problem. The two solutions give almost exactly the same prediction of the MSD saturation value. But the full solutions might have some differences we did not realize in the past. In this note, we discuss this issue and try to reconcile the two solutions.

##### Formulation

The formulations are almost the same, given some conversions between different notations.

Maggi 2014:

$$
\dot y = -\mu ky + \eta^T + \eta^A
$$

where $\eta^A$ is the active noise, satisfying $\left< \eta^A(t)\eta^A(t') \right>=(D_A/\tau)e^{-|t-t'|/\tau}$.

Cristian:

$$
\dot y = -\gamma y + \eta^A
$$

where $\eta^A$ is the active noise, satisfying $\left< \eta^A(t)\eta^A(t') \right>=Ae^{-|t-t'|/\tau}$.

If we let the "constants" $\mu k = \gamma$ and $D_A/\tau=A$, the two formulations are exactly the same.

##### Solutions (only look at the active terms)

Maggi 2014:

$$
\left< \Delta y^2(t) \right> = \frac{2D_A}{\mu k} \frac{1-e^{-\mu kt} - \mu k\tau(1-e^{-t/\tau})}{1-(\mu k\tau)^2}
$$

Cristian:

$$
\left< \Delta y^2(t) \right> = \frac{2A}{\gamma+1/\tau}(\frac{1-e^{-2\gamma t}}{2\gamma} - \frac{e^{-(\gamma+1/\tau)t} - e^{-2\gamma t}}{\gamma - 1/\tau})
$$

##### Long time limit ($t\to\infty$)

Maggi 2014:

$$
\lim_{t\to\infty} \left< \Delta y^2(t) \right>  = \frac{2D_A}{\mu k} \frac{1 - \mu k\tau}{1-(\mu k\tau)^2} = \frac{2D_A}{\mu k(1+\mu k \tau)}
$$

Cristian:

$$
\lim_{t\to\infty}\left< \Delta y^2(t) \right> = \frac{2A}{\gamma+1/\tau}(\frac{1}{2\gamma} - \frac{0-0}{\gamma - 1/\tau}) = \frac{A}{\gamma(\gamma + 1/\tau)}
$$

By doing the notation conversions in the previous section ($\mu k = \gamma$ and $D_A/\tau=A$), we can convert the solution of Maggi 2014 to

$$
\frac{2D_A}{\mu k(1+\mu k \tau)} = \frac{2D_A/\tau}{\gamma(\gamma+1/\tau)} = \frac{2A}{\gamma(\gamma + 1/\tau)}
$$

which is similar to Cristian's limit solution, but off by a factor of 2.

##### Zero-memory limit ($\tau\to 0$)

When the correlation time of active noise $\tau=0$, the noise becomes equivalent to a white noise, and the model is expected to recover the "Brownian motion in a harmonic potential", which takes the following form:

$$
\left< \Delta y^2(t) \right> = \frac{2D_T}{\mu k} (1 - e^{-\mu kt})
$$

Now let's bring $\tau\to0$ for both solutions.

Maggi 2014:

$$
\lim_{\tau\to0} \left< \Delta y^2(t) \right> = \frac{2D_A}{\mu k}  \frac{1-e^{-\mu kt} - 0}{1-0} = \frac{2D_A}{\mu k} (1-e^{-\mu kt})
$$

Cristian:

$$
\lim_{\tau\to0} \left< \Delta y^2(t) \right> =  \lim_{\tau\to0}\frac{2A}{\gamma+1/\tau}(\frac{1-e^{-2\gamma t}}{2\gamma})
$$

If we assume $A$ is finite, the limit MSD, $\lim_{\tau\to0} \left< \Delta y^2(t) \right>=0$.

##### We can still recover a valid zero-memory formulation, which implies $A\to\infty$

Let's do the notation conversions in the previous section ($\mu k = \gamma$ and $D_A/\tau=A$) on the limit solution:

$$
\frac{2A}{\gamma+1/\tau}(\frac{1-e^{-2\gamma t}}{2\gamma}) = \frac{2A\tau}{\gamma\tau+1}(\frac{1-e^{-2\gamma t}}{2\gamma}) = \frac{2D_A}{\gamma\tau+1}(\frac{1-e^{-2\gamma t}}{2\gamma})
$$

Now if we take the limit $\tau\to0$, we get

$$
\lim_{\tau\to0} \frac{2D_A}{\gamma\tau+1}(\frac{1-e^{-2\gamma t}}{2\gamma}) = \frac{D_A}{\gamma}(1-e^{-2\gamma t})
$$

The "Brownian motion in a harmonic potential" limit is recovered. If we assume $D_A$ a constant, then $A=D_A/\tau \to \infty$ in the zero-$\tau$ limit.
