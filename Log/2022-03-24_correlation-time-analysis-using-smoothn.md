---
layout: "post"
title: "correlation time analysis using smoothn"
date: "2022-03-24 12:57"
---

### Correlation time analysis using `smoothn`

Using `smoothn`, most noisy VACF curves can be smoothed adaptively. The 01172022 data are shown below as an example.

![0117 compare vacf calculation](../images/2022/03/0117-compare-vacf-calculation.png)

The curves are fitted with exponential decay to obtain the correlation time $\tau$.

![vacf fitting repo](../images/2022/03/vacf-fitting-repo.png)

The fitting curves are saved for future quality check in a .zip archived stored on Google Drive.

![zip file of vacf](../images/2022/03/zip-file-of-vacf.png)

We hypothesized that the correlation time is correlated with the bacterial activity. Below I plot correlation time against mean velocity to visualize this correlation.

![tau vs mean velocity](../images/2022/03/tau-vs-mean-velocity.png)
