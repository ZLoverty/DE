### Protocol: bacteria in porous media

This protocol describes the motility assay of _E. coli_ in 2D porous media.

##### Edit
- Aug 2, 2022: First version.
- Aug 11, 2022: More details added after a few days of practice, 2-color imaging in particular.

##### 1. Ingredients

- Fluorinert FC-40 oil droplets (3 $\mu$m and 10 $\mu$m in diameter)
- 5 mM SDS solution
- swimming pool 54 $\mu$m height
- several 1.5 ml eppendorf tubes
- 18 mm x 18 mm glass coverslips
- AD62 (or AD63) bacterial culture

![ingred](../images/2022/08/ingred.png)

##### 2. Protocol

**Prepare bacteria-droplet mixture**

_Note: numbers are for 3 (10) $\mu$m droplets_

1. Transfer 195 (180) $\mu$l SDS solution to an eppendorf tube.
2. From the big droplet vial, transfer 5 (20) $\mu$l droplets to the SDS solution.

_Note: let droplet suspension rest for several hours so that all droplets sediment to the bottom of the vial. Take droplets from the upper part of the sediment._

![take droplets here](../images/2022/08/take-droplets-here.png)

3. Mix well by stirring with a pipette tip. Do NOT mix by pipetting up and down because it likely causes coalescence.
4. Transfer 180 $\mu$l droplet suspension to another eppendorf tube.
5. Transfer 20 $\mu$l bacterial suspension (OD $\approx 0.2$) to the droplet suspension (final OD $\approx 0.02$).

_Note: for each sample, prepare a fresh dilution from the original bacterial suspension (which is washed by centrifugation and is not yet diluted). This gives good motility._

6. Now we have 200 $\mu$l of bacteria-droplet mixture.

**Load mixture to the swimming pool**

1. Carefully spread 100 $\mu$l mixture on the bottom substrate of the swimming pool, make sure to cover all the surface.
2. Cover the coverslip at a 45$^\circ$ angle, to avoid trapping air bubbles in the pool.

![coverslip](../images/2022/08/coverslip.png)

3. Move the coverslip to cover the whole pool.

![coverslip 2](../images/2022/08/coverslip-2.png)

4. Clean the leftover liquid with tissue.
5. (Optional) Cover the coverslip edges with glycerol to avoid evaporation. Only do this when using long WD lenses, like 20X or 40X. For 63X, this is not possible because the substrate glass of the swimming pool thickness is 500 um, larger than the WD of the lens (~400 um). It's possible to invert the specimen to observe through the coverslip. However, evaporation happens earlier compared to samples covered by glycerol.

**Imaging - confocal**

1. We use the confocal microscope at Gulliver lab to image. Set the focal plane at the equatorial plane of the droplets sitting on the bottom substrate.
2. Set exposure time to 100 ms.
3. Use blue laser of intensity 30-50%.
4. In Ti Pad tab, turn off the bright light lock and adjust bright light so that we can see both droplets configuration and fluorescent bacteria.
5. Take videos of 3000 frames each using Fast Time Lapse (5 min videos).

**Imaging - two color**

1. First fill the pool with just bacterial suspension to: i) chcek motility, ii) adjust focal plane to the correct position to speed the following tests.
2. Put the beam splitter set in place to the two color imaging.
3. Load bacteria-droplet mixture sample, turn on red and violet fluorescent light and set filter to 90 HE DAPI.
4. Adjust the light intensity to have an satisfactory contrast.

Note: the noise level of the tracking device is around 100-200. In order to have a good contrast, the max intensity of the fluorescence should be >500.

5. Turn off the fluorescent light. Adjust the bright field light so that the droplet packing structure is visible.
6. Turn on fluorescent light again, find a region of desired droplet structure. Take videos of 3000 frames (10 fps, 5 min).

#### Appendix

##### A. Porous media preparation

The porous media used in this experiment are mono-dispersed droplets of Fluorinert FC-40 (an immiscible fluorocarbon oil). The density of FC-40 is 1.85 g/ml, so it sediments in water due to gravity. 5 ml FC-40 is pressed through a porous membrane to 20 ml SDS solution (5 mM), forming a dense droplet suspension.

##### B. Swimming pool details

- The bottom substrate is 2-inch circular borofloat glass wafer, 500 $\mu$m thick.
- The square wall is made by photoresist SU-8 2050 (Microchem). Outer side length is 20 cm, while inner side length is 15 cm.
- The pool height is 54 $\mu$m.

![swimming pool](../images/2022/08/swimming-pool.png)
