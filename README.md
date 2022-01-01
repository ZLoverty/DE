![cover](Illustrations/project-cover/v0.png)
# DE

DE stands for Double Emulsion.
It's the experimental system I am working with at PMMH-ESPCI with Eric Clement, Anke Lindner and Teresa Lopez-Leon.
The project is a combination of the double emulsion system and active matter.
In particular, I will be studying
- "Thermometer" in an active bath
- ...

In this repository, I save the notes, code, illustrations and eventually the draft for the research paper of this project.

**Some structural edits:**
- Dec 15, 2021 -- i) use main readme.md for to-do's, ii) put notes in *obsidian* style, i.e. .md's in the Notes folder and all images mix in *img* folder.

## To-do list
- [Analysis of collective motions in droplets](Notes\Analysis_of_collective_motions_in_droplets.md)
  - **PIV should be run again with `PIV_masked()` instead of `piv_drop`, batch script needs to be implemented**
  - **compare BF and fluorescence image PIV**
  - **temporal evolution of velocity: does bacterial activity decay with time in droplets? What's the typical time scale?**
  - spatial autocorrelation length: this can be the first observable for temporal activity evolution
  - temporal autocorrelation
  - order parameter: any oscillatory motions detected?

- experiment
  - if we see an oscillatory motion at the equator, we should be able to see it on one side too!
- data
  - have all the `NothingToSay` Drive backed up and try to use a merged file system solution, such as [mergerfs](https://github.com/trapexit/mergerfs)
  - validity of PIV measurement, the velocity seems to be too small.

Although it's important to determine the best PIV parameters, it's not a trivial work and significantly delay the downstream analysis. Therefore, I will proceed with the current PIV data, and come back to the question of best parameters when the whole analysis work flow is set up.

## "Thermometer" in an active bath

#### Project summary

We devise a "thermometer" for an active bath using double emulsions.
Specifically, we confine swimming *E. coli* bacteria in the aqueous phase of oil/water/oil double emulsions and examine the motions of the inner oil droplets.
Surrounded by swimming bacteria, the inner oil droplets exhibit stronger fluctuations, deviating from familiar Brownian motion.
In this study, we combine microfluidic techniques and advanced imaging techniques to investigate:
- generalized temperature in active matter systems
- whether boundary conditions, especially curvature, affect the temperature
- to what extent thermodynamic tools can be generalized to active matter systems

## Collective motion in droplets

## Sliding on soft interface

## Wobbling in droplets

## Structure of this repos
```
|- DE
  README.md
  |- Code
  |- Illustrations
  |- Notes
  |- (Draft)
  |- Log
  |- Protocols
  |- MSCA (the EU commission Marie Curie fellowship proposal)
```
