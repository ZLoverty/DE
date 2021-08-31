# Diffusivity and Effective Temperature
One objective of DE project is to measure the effective "temperature" of an active bath.

The motion of a passive object provides information about a system.
For example, in [Stokes-Einstein relation](https://en.wikipedia.org/wiki/Einstein_relation_(kinetic_theory)), the diffusivity of a spherical particle through a viscous liquid is a measure of temperature.
Wu and Libchaber (2000) showed that the diffusion of a sphere in bacterial suspensions is much stronger than its Brownian motion.
If the diffusivity is used to calculate the effective temperature, it is \~100 times higher than room temperature.
~They also observed that a he diffusion coefficient has 1/R dependence on particle size R.~



Combine this previous knowledge and our DE system, it becomes interesting to see if the size of a confining droplet (the outer droplet) also changes the effective temperature.
To investigate this topic further, we measure the diffusivity of inner droplets of fixed size within confining droplets of various sizes.

## Some Questions

### 1. Is Temperature well defined in active systems? [Yes, under certain conditions]

Equilibrium states can be accurately described by a small number of thermodynamic variables, such as temperature and pressure.
In contrast, such framework does not exist for out-of-equilibrium systems.
Efforts have been made to generalize temperature and pressure to active matter systems,
and it has been shown that **effective temperature can be used** when certain conditions are met:

- **long observation time:** passive tracer show diffusive motions only at long lag times (compared to active particle swimming time scale)
- **Boltzmann statistics holds:** the position distribution should be exponential function of potential energy. Active matter breaks detailed balance, so Boltzmann statistics does not necessarily hold. The break-down of Boltzmann statistics is most evident when specially designed boundaries breaks the symmetry of active bath, such as the rectification effects and spontaneous flow in microchannels. For examples, see Refs.[11]-[20] in [Maggi 2014](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.113.238303).

### 2. What PDF do we expect to see in our DE systems?

We analyze **position** and **displacement** PDFs in **xy** and **z**.
4 different combinations are to be addressed.
- **Position xy:** in small motion limit, should be Gaussian because of the spring-like restoration force
- **Position z:** Boltzmann with gravitational potential
- **Displacement xy:** UK
- **Displacement z:** UK

What is the difference between position and displacement PDFs? [They are the same when \<x\>=0]

### 3. What if Boltzmann distribution does not hold?

- Is my PDF(z) data convincing enough?
- This is where we are. How do we proceed?

## Probability Density Functions (PDF)

We measure the statistics of inner droplet motions, including z position PDF and displacement PDF, to get effective temperature.
These PDFs will also tell us how much the system deviates from equilibrium.

### Z Position PDF

Think of the inner droplet as a molecule in gravitational potential in z direction.
The z position PDF takes **Boltzmann distribution**: P(z)=P0*exp(-E/kT), where E is the potential energy of a certain state (z).

The figure below shows the PDF(z) of "small" (left) and "big" (right) inner droplets.
Thinner gray lines are different runs of experiment and thicker black lines are the averages.
The insets show the photos of the double emulsions, as well as the trajectories of the inner droplets.
Two observations: (i) PDF(z) of "big" inner droplet is more similar to Boltzmann distribution; (ii) the effective temperature (obtained by fitting the PDF with linear function) is on the order to 10^4 K.

![PDFz](pdfz.png)

### Displacement PDF

Non-Gaussianity is a characteristic of displacement PDF of tracers in active bath (Leptos 2009).
I measured the displacement PDF of small inner droplets (r = 4.5 um).
~I don't know how to interpret these PDF since they result from combined effects of active stress and buoyancy potential.~

![PDFdx](pdf-dx.png)

## Mean Square Displacement (MSD)

### 2D or 3D
2D MSD (XY motion) and 3D MSD (XYZ motion) are usually very similar, because the motion in z is much weaker than in XY.
This is consistent with the results from Cristian, as shown below.

![MSD-xyz](MSD-xyz.png)


### Droplet Size Effect
The diffusion of inner droplets varies drastically from experiment to experiment.
Potential control parameters are **outer droplet size (R)**, **inner droplet size (r)** and **bacterial concentration (n)**. These parameters are indicated in the legend as R/r[n]

So far, 3 sets of control parameters have been tested.
In the figure below, I plot the 2D MSD's of these experiments.

![MSD 3 experiments](MSD-multi.png)

The data show potential concentration-diffusivity and dropsize-diffusivity correlations.
To draw quantitative conclusion, better parameter control is needed.
