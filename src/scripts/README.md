# High Variable Plotting

This section describes the `high_var.sh` tool

<details>
<summary><h2>High Variable Plotting</h2></summary>

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

<details>
<summary><h2>Configuration Details</h2></summary>

<details>
<summary><h3>Database Settings</h3></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `file.db_path` | `os.getcwd()` | Path to database directory |
| `file.default_db` | `"celloutput.visit"` | Default database filename |
| `file.height` | `"1080"` | Output image height in pixels |
| `file.output_filename` | `"high_var_all_time"` | Output file name for generated visualizations |
| `file.width` | `"1080"` | Output image width in pixels |

</details>

<details>
<summary><h3>High Var</h3></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `high_var.mode` | `"space"` | The 2 different modes for the high_var.sh script, see the high var section for details, the two options are time and space |

</details>

<details>
<summary><h3>Plotting Configuration (Variables, legend, location, etc.)</h3></summary>

<details>
<summary><h4>Background Img</h4></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.background_img.name` | `"path/to/img/img.png"` | Path to background image |
| `plotting.background_img.on` | `"0"` | Enable a background image instead of a background variable |

</details>

<details>
<summary><h4>Background Var</h4></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.background_var.colormap` | `"gray"` | Background colormap |
| `plotting.background_var.invert` | `"0"` | Invert background colors (0=off, 1=on) |
| `plotting.background_var.name` | `"eta"` | Background variable name |
| `plotting.background_var.on` | `"0"` | Enable background variable (0=off, 1=on) |

</details>

<details>
<summary><h4>Contour</h4></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.contour.color` | `(0, 0, 0, 255)` | Contour color (RGBA) (default: black) |
| `plotting.contour.linewidth` | `"2"` | Contour line width |
| `plotting.contour.on` | `"0"` | Enable contour lines (0=off, 1=on) |
| `plotting.contour.values` | `"0.5"` | Contour value(s) |

<details>
<summary><h5>Var</h5></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.contour.var.name` | `"phi"` | Variable to contour |

</details>

</details>

<details>
<summary><h4>Legend</h4></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.legend.on` | `"0"` | Enable legend (0=off, 1=on) |
| `plotting.legend.position` | `"right"` | Legend X position (left/right/top/bottom) |

<details>
<summary><h5>Name</h5></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.legend.name.fontsize` | `"8"` | Legend font size |
| `plotting.legend.name.on` | `"0"` | Enable legend name/label (0=off, 1=on) |
| `plotting.legend.name.text` | `"Good Legend"` | Legend text |

</details>

<details>
<summary><h5>Ticks</h5></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.legend.ticks.fontsize` | `"10"` | fontsize of the ticks in the colorbar |
| `plotting.legend.ticks.numticks` | `"5"` | Number of ticks in the colorbar |

</details>

</details>

<details>
<summary><h4>Main Plotting Var</h4></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.main_plotting_var.colormap` | `"plasma"` | Colormap for visualization, see available colormaps section for support VisIt colormaps |
| `plotting.main_plotting_var.max` | `"2000"` | Maximum value for color scale |
| `plotting.main_plotting_var.min` | `"0"` | Minimum value for color scale |
| `plotting.main_plotting_var.name` | `"temp"` | Variable to plot |

<details>
<summary><h5>Define Scalar Expression</h5></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.main_plotting_var.define_scalar_expression.expression` | `"expression_here"` | Mathematical expression definition |
| `plotting.main_plotting_var.define_scalar_expression.name` | `"expression_name"` | Name for the expression |
| `plotting.main_plotting_var.define_scalar_expression.on` | `"0"` | Enable custom scalar expression (0=off, 1=on) |

</details>

<details>
<summary><h5>Thresholding</h5></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.main_plotting_var.thresholding.on` | `"0"` | Enable thresholding (0=off, 1=on) |

<details>
<summary><h6>Var</h6></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.main_plotting_var.thresholding.var.max` | `"1e37"` | Maximum threshold value |
| `plotting.main_plotting_var.thresholding.var.min` | `"0.0"` | Minimum threshold value |
| `plotting.main_plotting_var.thresholding.var.name` | `"eta"` | Variable to threshold by |

</details>

</details>

</details>

</details>

<details>
<summary><h3>Data Transfer, not for input use</h3></summary>

<details>
<summary><h4>Time</h4></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `sim.time.arr` | `"0"` | not a user input, used to transfer data between scripts, will get overwritten if included in input file |

</details>

</details>

<details>
<summary><h3>Step Control</h3></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `step.end` | `"-1"` | Ending timestep (-1 = all timesteps) |
| `step.interval` | `"1"` | Interval between timesteps |
| `step.start` | `"0"` | Starting timestep |

</details>

</details>

<details>
<summary><h2>Available Colormaps</h2></summary>

The following colormaps are supported for visualization:

### Sequential Colormaps
- `viridis`
- `plasma`
- `magma`
- `inferno`
- `cividis`
- `turbo`
- `hot`

### Grayscale
- `gray`

### Single Hue Sequential
- `blues`
- `Greens`
- `Oranges`
- `Purples`
- `Reds`

### Multi-Hue Sequential
- `BuGn`
- `GnBu`
- `PuBu`
- `PuBuGn`
- `OrRd`
- `PuRd`
- `RdPu`
- `YlgGn`
- `YlGnBu`
- `YlOrBr`
- `YlOrRd`

### Diverging Colormaps
- `PRGn`
- `PiYG`
- `PuOr`
- `RdBu`
- `RdGy`
- `RdYlBu`
- `RdYlGn`
- `Spectral`

### Qualitative Colormaps
- `rainbow`
- `Dark2`
- `Paired`
- `Set1`

</details>

## Notes

- Boolean parameters use `0` for off/disabled and `1` for on/enabled
- Color values are specified as RGBA tuples with values 0-255
- Use `-1` for `step.end` to process all available timesteps
