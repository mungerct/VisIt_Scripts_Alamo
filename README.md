# High Variable Plotting

This section describes the `high_var.sh` tool

<details>
<summary><h2>High Variable Plotting</h2></summary>

This code produces a compiled image the highest variable over all timesteps, the example image below shows how temperature timesteps can be combined to visualize where the highest temperature in a given simulation is over all time. 

![Make High Temp Plot Example](/examples/make_high_temp_plot_example/Make_High_Temp_Plot_Example.svg)

The code saves images at all specified timesteps, and then overlays them and compares their values, the larger of the two values is kept so only the higher temperature is shown in the result.

</details>

# Configuration Defaults

This section describes the default configuration values for the visualization toolbox.

<details>
<summary><h2>Configuration Details</h2></summary>

<details>
<summary><h3>Database Settings</h3></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `file.db_path` | `os.getcwd()` | Path to database directory |
| `file.default_db` | `"celloutput.visit"` | Default database filename |
| `file.output_filename` | `"high_var_all_time"` | Output file name for generated visualizations |
| `file.width` | `1080` | Output image width in pixels |
| `file.height` | `1080` | Output image height in pixels |

</details>

<details>
<summary><h3>Step Control</h3></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `step.interval` | `1` | Interval between timesteps |
| `step.start` | `0` | Starting timestep |
| `step.end` | `-1` | Ending timestep (-1 = all timesteps) |

</details>

<details>
<summary><h3>Main Plotting Variable</h3></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.main_plotting_var.name` | `"temp"` | Variable to plot |
| `plotting.main_plotting_var.colormap` | `"plasma"` | Colormap for visualization, see available colormaps section for support VisIt colormaps |
| `plotting.main_plotting_var.min` | `0` | Minimum value for color scale |
| `plotting.main_plotting_var.max` | `2000` | Maximum value for color scale |

<details>
<summary><h4>Scalar Expression (Optional)</h4></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.main_plotting_var.define_scalar_expression.on` | `0` | Enable custom scalar expression (0=off, 1=on) |
| `plotting.main_plotting_var.define_scalar_expression.name` | `"expression_name"` | Name for the expression |
| `plotting.main_plotting_var.define_scalar_expression.expression` | `"expression_here"` | Mathematical expression definition |

</details>

<details>
<summary><h4>Thresholding</h4></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.main_plotting_var.thresholding.on` | `0` | Enable thresholding (0=off, 1=on) |
| `plotting.main_plotting_var.thresholding.var.name` | `"eta"` | Variable to threshold by |
| `plotting.main_plotting_var.thresholding.var.min` | `0.0` | Minimum threshold value |
| `plotting.main_plotting_var.thresholding.var.max` | `1e37` | Maximum threshold value |

</details>

</details>

<details>
<summary><h3>Background Variable</h3></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.background_var.on` | `0` | Enable background variable (0=off, 1=on) |
| `plotting.background_var.name` | `"eta"` | Background variable name |
| `plotting.background_var.invert` | `0` | Invert background colors (0=off, 1=on) |
| `plotting.background_var.colormap` | `"gray"` | Background colormap |

</details>

<details>
<summary><h3>Contours</h3></summary>

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.contour.on` | `0` | Enable contour lines (0=off, 1=on) |
| `plotting.contour.var.name` | `"phi"` | Variable to contour |
| `plotting.contour.values` | `0.5` | Contour value(s) |
| `plotting.contour.linewidth` | `2` | Contour line width |
| `plotting.contour.color` | `(0, 0, 0, 255)` | Contour color (RGBA) |

</details>

<details>
<summary><h3>Legend</h3></summary>

Only supported for `high_var.sh`

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.legend.name.on` | `0` | Enable legend (0=off, 1=on) |
| `plotting.legend.name.text` | `"Good Legend"` | Legend text |
| `plotting.legend.name.position.x` | `-1150` | Legend X position |
| `plotting.legend.name.position.y` | `-800` | Legend Y position |
| `plotting.legend.name.dpi` | `500` | Legend resolution (DPI) |
| `plotting.legend.name.fontsize` | `8` | Legend font size |

</details>

<details>
<summary><h3>Available Colormaps</h3></summary>

The following VisIt colormaps are supported for visualization:

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
- `BuGn` (Blue-Green)
- `GnBu` (Green-Blue)
- `PuBu` (Purple-Blue)
- `PuBuGn` (Purple-Blue-Green)
- `OrRd` (Orange-Red)
- `PuRd` (Purple-Red)
- `RdPu` (Red-Purple)
- `YlGn` (Yellow-Green)
- `YlGnBu` (Yellow-Green-Blue)
- `YlOrBr` (Yellow-Orange-Brown)
- `YlOrRd` (Yellow-Orange-Red)

### Diverging Colormaps
- `PRGn` (Purple-Green)
- `PiYG` (Pink-Yellow-Green)
- `PuOr` (Purple-Orange)
- `RdBu` (Red-Blue)
- `RdGy` (Red-Gray)
- `RdYlBu` (Red-Yellow-Blue)
- `RdYlGn` (Red-Yellow-Green)
- `Spectral`

### Qualitative Colormaps
- `rainbow`
- `Dark2`
- `Paired`
- `Set1`

</details>

<details>
<summary><h3>Notes</h3></summary>

## Notes

- Boolean parameters use `0` for off/disabled and `1` for on/enabled
- Color values are specified as RGBA tuples with values 0-255
- Use `-1` for `step.end` to process all available timesteps

</details>
</details>