# Configuration Defaults

This document describes the default configuration values for the visualization tool.

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
| `high_var.mode` | `"time"` | The 2 different modes for the high_var.sh script, see the high var section for details, the two options are time and space |

</details>

<details>
<summary><h3>Plotting Configuration</h3></summary>

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
<summary><h3>Sim</h3></summary>

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
