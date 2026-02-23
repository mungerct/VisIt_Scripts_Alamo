# Overview

This git repo provides a framework to use VisIt to analyse the results of scientific simulations in a reproducible and systemic way. Currently there are 2 main functionalities of the repo, "high variable plotting" and making gifs. The high variable plotting is meant to collapse a 3 dimensional simulations (2 length axis and 1 time axis) into a 2d image, removing the time dimension to be used in publications. This can be used to see the highest temperature at each cell over the course of a simulation (see example below) or to find where the highest stress in a simulated domain occurs at. The make gifs section of the repo makes a gif to be used in presentations of your data. Both of these options use .txt files as input files (see sample inputs below) and a metadata file with all parameters and the git hash is saved after every image/gif is made. This is meant to make all figures reproducible, speeding up research so if you forget how you made an image, the metadata will allow you to remake it. Below is a summary of the "high_var.sh" and "make_gif.sh" shell scripts that are used to run this code.


# High Variable Plotting

This section describes the `high_var.sh` tool

<details>
<summary><h3>High Variable Plotting</h3></summary>

To use this feature, the `high_var.mode = space` must be specificed in the input deck. This mode "spacially" adds a value and takes the highest value at each spacial point over time. This code produces a compiled image the highest variable over all timesteps, the example image below shows how temperature timesteps can be combined to visualize where the highest temperature in a given simulation is over all time. 

![Make High Temp Plot Example](/examples/make_high_temp_plot_example/Make_High_Temp_Plot_Example.svg)

The code saves images at all specified timesteps, and then overlays them and compares their values, the larger of the two values is kept so only the higher temperature is shown in the result. The input file used to make the above image is provided below as an example.
<details>
<summary><h2>Sample Script</h2></summary>

``` file.db_path: /research/papers/RegressionWithVoidsFullFeedback/results/arbitary_geometry_tests/output.arbitary_geo.phi_fake_grain
file.default_db: celloutput.visit
file.output_filename: make_high_temp_fig_composite
step.interval: 10
step.start: 20
step.end: 51
plotting.main_plotting_var.name: temp
plotting.main_plotting_var.colormap: hot
plotting.main_plotting_var.min: 700
plotting.main_plotting_var.max: 1200
plotting.main_plotting_var.thresholding.on: 1
plotting.main_plotting_var.thresholding.var.name: eta
plotting.main_plotting_var.thresholding.var.min: 0.5
plotting.main_plotting_var.thresholding.var.max: 1e+37
plotting.background_var.on: 1
plotting.background_var.name: eta
plotting.background_var.invert: 0
plotting.background_var.colormap: gray
plotting.legend.name.on: 1
plotting.legend.name.text: Temp (K)
plotting.legend.name.position.x: -1150
plotting.legend.name.position.y: -800
plotting.legend.name.dpi: 500
plotting.legend.name.fontsize: 4
```
This file was run using the following command
```
~/path/to/VisIt_Scripts_Alamo/high_var.sh /path/to/input/file/input.txt
```

</details>

To use this feature, the `high_var.mode = time` must be specificed in the input deck. This "temporally" adds all of the plots togeather, taking the points from larger time values at each spacial point. The example below is from the burning of a propellant, and the "burn front" can be seen as time increases. The different colors coorspond to the edge of the burned region at each time value.
![Make eta_reg Example](/examples/make_high_temp_plot_example/eta_reg.png)

<details>
<summary><h2>Sample Script</h2></summary>

```
file.db_path: /research/papers/RegressionWithVoidsFullFeedback/results/arbitary_geometry_tests/output.arbitary_geo.phi_fake_grain
file.default_db: celloutput.visit
file.output_filename: eta_reg
file.width: 1080
file.height: 1080
step.interval: 10
step.start: 0
step.end: 151
plotting.main_plotting_var.name: eta
plotting.main_plotting_var.colormap: plasma
plotting.main_plotting_var.min: 0
plotting.main_plotting_var.max: 1
plotting.main_plotting_var.thresholding.on: 1
plotting.main_plotting_var.thresholding.var.name: eta
plotting.main_plotting_var.thresholding.var.min: 0.5
plotting.main_plotting_var.thresholding.var.max: 1
plotting.background_var.on: 1
plotting.background_var.name: eta
plotting.background_var.invert: 0
plotting.background_var.colormap: gray
plotting.contour.on: 1
plotting.contour.var.name: phi
plotting.contour.values: (0.25, 0.5, 0.75)
plotting.contour.linewidth: 1
plotting.contour.color: (0, 0, 0, 255)
plotting.legend.on: 1
plotting.legend.position: bottom
plotting.legend.name.on: 1
plotting.legend.name.text: Time (s)
plotting.legend.name.fontsize: 8
sim.time.arr: [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75]
high_var.mode: time
```

</details>
</details>