---
layout: "post"
title: "active motion in a harmonic trap"
date: "2022-04-29 12:55"
---

### Literature review -- active motion in a harmonic trap

The motion of passive particles driven by an active bath results from a combined effect of hydrodynamic interaction and collision between many pairs of passive particles and active particles in the bath. Despite the complexity of these interactions, the resulting motion is usually pretty well captured by a simple stochastic model where the contribution from the active bath is considered as a noise with some persistence (Wu and Libchaber 2000). In such a model, the motion of passive particles in an active bath resembles that of active Brownian particles.

How active baths transfer momentum to passive particles remain poorly understood. Intuitively, higher concentration and activity lead to higher motility of the driven passive particle. Mino et al. 2011 proposed a "active flux" model, which states that the diffusivity grows linearly with concentration $n$ and velocity $V$:

$$
D = D_0 + \beta n V.
$$

However, this model does not account for the size-dependent diffusivity (Patteson 2016) and potential-dependent diffusivity (Ye 2020). **Our experiment may also reveal a curvature-dependent diffusivity**. Clearly, the momentum transfer process is more complicated than the model above.

##### Dynamics of active particles in a harmonic potential

There are several studies on the dynamics of active particles in a harmonic potential: Tailleur and Cates 2009 (1-D RTP model), Takatori 2016 (Janus particle in acoustic trap), Dauchot and Deremy 2019 (hexbug in a parabolic dish) and Schmidt 2021 (gold nanoparticle in optical trap). All of these works report position distributions significantly deviating from Boltzmann. Such deviation can be understood by considering the persistence length $l_p$ and the characteristic trap length $l_{trap}$: when $l_p \ll l_{trap}$, the motion remains random, so the position distribution is Boltzmann; when $l_p \ge l_{trap}$, each run of active particle can reach the very edge of the potential, leading to a high-potential peak.

An interesting **orbital motion** is reported for nanoparticles and macroscopic robots (Schmidt 2021 and Dauchot 2019), but not for micron-size particles.

##### Dynamics of passive particle in an active bath in a harmonic potential

The dynamics of passive particle in an active bath has also been studied, in particular the position distributions (Maggi 2014, Argun 2016). In this case the deviation from Boltzmann distribution is less significant: the large displacement tails are heavier, but the general center-peak distribution persists. 

##### Multi-particle interaction mediated by an active bath

Multi-particle interaction mediated by an active bath, a more complex scenario, has also been investigated (Angelani 2011, Gokhale 2021). We may borrow ideas from them to study the interaction in curved spaces.

### References

Wu, Xiao-Lun, and Albert Libchaber. “Particle Diffusion in a Quasi-Two-Dimensional Bacterial Bath.” Physical Review Letters 84, no. 13 (March 27, 2000): 3017–20. https://doi.org/10.1103/PhysRevLett.84.3017.

Miño, Gastón, Thomas E. Mallouk, Thierry Darnige, Mauricio Hoyos, Jeremi Dauchet, Jocelyn Dunstan, Rodrigo Soto, Yang Wang, Annie Rousselet, and Eric Clement. “Enhanced Diffusion Due to Active Swimmers at a Solid Surface.” Physical Review Letters 106, no. 4 (January 25, 2011): 048102. https://doi.org/10.1103/PhysRevLett.106.048102.


Patteson, Alison E., Arvind Gopinath, Prashant K. Purohit, and Paulo E. Arratia. “Particle Diffusion in Active Fluids Is Non-Monotonic in Size.” Soft Matter 12, no. 8 (2016): 2365–72. https://doi.org/10.1039/C5SM02800K.

Ye, Simin, Peng Liu, Fangfu Ye, Ke Chen, and Mingcheng Yang. “Active Noise Experienced by a Passive Particle Trapped in an Active Bath.” Soft Matter 16, no. 19 (May 21, 2020): 4655–60. https://doi.org/10.1039/D0SM00006J.

Tailleur, J., and M. E. Cates. “Sedimentation, Trapping, and Rectification of Dilute Bacteria.” EPL (Europhysics Letters) 86, no. 6 (June 1, 2009): 60002. https://doi.org/10.1209/0295-5075/86/60002.

Takatori, Sho C., Raf De Dier, Jan Vermant, and John F. Brady. “Acoustic Trapping of Active Matter.” Nature Communications 7, no. 1 (March 10, 2016): 10694. https://doi.org/10.1038/ncomms10694.

Dauchot, Olivier, and Vincent Démery. “Dynamics of a Self-Propelled Particle in a Harmonic Trap.” Physical Review Letters 122, no. 6 (February 13, 2019): 068002. https://doi.org/10.1103/PhysRevLett.122.068002.

Schmidt, Falko, Hana Šípová-Jungová, Mikael Käll, Alois Würger, and Giovanni Volpe. “Non-Equilibrium Properties of an Active Nanoparticle in a Harmonic Potential.” Nature Communications 12, no. 1 (March 26, 2021): 1902. https://doi.org/10.1038/s41467-021-22187-z.

Maggi, Claudio, Matteo Paoluzzi, Nicola Pellicciotta, Alessia Lepore, Luca Angelani, and Roberto Di Leonardo. “Generalized Energy Equipartition in Harmonic Oscillators Driven by Active Baths.” Physical Review Letters 113, no. 23 (December 3, 2014): 238303. https://doi.org/10.1103/PhysRevLett.113.238303.

Argun, Aykut, Ali-Reza Moradi, Erçaǧ Pinçe, Gokhan Baris Bagci, Alberto Imparato, and Giovanni Volpe. “Non-Boltzmann Stationary Distributions and Nonequilibrium Relations in Active Baths.” Physical Review E 94, no. 6 (December 29, 2016): 062150. https://doi.org/10.1103/PhysRevE.94.062150.

Angelani, L., C. Maggi, M. L. Bernardini, A. Rizzo, and R. Di Leonardo. “Effective Interactions between Colloidal Particles Suspended in a Bath of Swimming Cells.” Physical Review Letters 107, no. 13 (September 19, 2011): 138302. https://doi.org/10.1103/PhysRevLett.107.138302.

Gokhale, Shreyas, Junang Li, Alexandre Solon, Jeff Gore, and Nikta Fakhri. “Dynamic Clustering of Passive Colloids in Dense Suspensions of Motile Bacteria.” ArXiv:2110.02294 [Cond-Mat, Physics:Physics], October 5, 2021. http://arxiv.org/abs/2110.02294.
