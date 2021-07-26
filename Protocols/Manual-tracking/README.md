# Manual Tracking

This protocol contains the standard procedure of tracking inner droplets using a combined method of crop-HoughCircles and manual tracking.

## Output file checklist

- **traj.csv**: 2D trajectory text file, use `crop-HoughCircles-Copy1.ipynb` to produce, and use `ImageJ Manual Tracking` to correct
- **xyz-traj.csv**: 3D trajectory text file, use `3D trajectory.ipynb` to produce
- **3d-traj-with-projections.png**: use `3D trajectory.ipynb` to produce
- **3d-traj-animation.avi**: use `3D trajectory.ipynb` to produce *.jpg, and use `ImageJ` to compose a video

## Steps

1. Run crop-HoughCircles tracking
2. Manually correct the tracking and save **traj.csv**
3. Combine **traj.csv** and **StagePositions.txt**, pay attention to the unit conversion, save **xyz-traj.csv**
4. Plot **3d-traj-with-projections.png**
5. Make **3d-traj-animation.avi**
