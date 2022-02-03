---
layout: "post"
title: "velocity autocorrelation"
date: "2022-02-03 14:02"
---

### Velocity autocorrelation

I've done this analysis in bulk. However, I notice that in a droplet this might be tricky because near the edge of a droplet, depending on the mask choice, there may be a ring of very low velocity. Such ring may affect the autocorrelation function. In this note, I use several real data to investigate how significant this effect is.

##### Samples: droplet#19, droplet#10, droplet#20

| Droplet# | Droplet size     | Bacterial concentration |
| :------------- | :------------- | :------------- |
| 19       | 28       |  185 |
| 10   | 85  | 197 |
| 20   |  112 | 185 |

##### Snapshots of samples

Note that we only take the first 10 s from each video, since later on the displacement of droplets may be significant.
