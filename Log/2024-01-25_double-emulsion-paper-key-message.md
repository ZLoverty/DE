---
date: 2024-01-25
author: Zhengyang Liu
title: double emulsion paper key message
---

# Double emulsion paper key message

We learn from our experiments that 

- confinement reduces the activity of bacterial suspensions, which can be quantified by the diffusivity of immersed passive object or PIV mean velocity;
- confinement reduces droplet lifetime, could be correlated with the first phenomenon.

We learn from analysis and simulation that

- the spring model is an approximation and is less accurate in measuring the activity of an active bath. We can improve the accuracy by matching experiment with simulation in a real sphere;

![picture 0](/assets/images/2024/01/v_fit.png)  

- interpolation improves the fit of MSD data;
- active flux model can be adapted to bring in geometrical factors, which can potentially help us collapse the D_b vs. OD data;
- PIV in XZ plane is problematic because it's sensitive to changes in the background. For example, the figure below shows a time series of mean PIV velocity. A big drop of mean velocity can be observed at around 50 s. After checking the video, I realize that there is another droplet out of focus sediments behind the droplet of interest. It creates a shadow in part of the droplet, and leads to a PIV velocity decrease.

![picture 1](/assets/images/2024/01/mean-velocity-drop.png)  
![picture 2](/assets/images/2024/01/shadow%20behind%20droplet.png)  
