# Configuration Defaults

This document describes the default configuration values for the visualization tool.

## Database Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| `file.db_path` | `os.getcwd()` | Path to database directory |
| `file.default_db` | `"celloutput.visit"` | Default database filename |
| `file.output_filename` | `"high_var_all_time"` | Output file name for generated visualizations |
| `file.width` | `1080` | Output image width in pixels |
| `file.height` | `1080` | Output image height in pixels |

## Step Control

| Parameter | Default | Description |
|-----------|---------|-------------|
| `step.interval` | `1` | Interval between timesteps |
| `step.start` | `0` | Starting timestep |
| `step.end` | `-1` | Ending timestep (-1 = all available) |

## Main Plotting Variable

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.main_plotting_var.name` | `"temp"` | Variable to plot |
| `plotting.main_plotting_var.colormap` | `"plasma"` | Colormap for visualization |
| `plotting.main_plotting_var.min` | `0` | Minimum value for color scale |
| `plotting.main_plotting_var.max` | `2000` | Maximum value for color scale |

### Scalar Expression (Optional)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.main_plotting_var.define_scalar_expression.on` | `0` | Enable custom scalar expression (0=off, 1=on) |
| `plotting.main_plotting_var.define_scalar_expression.name` | `"expression_name"` | Name for the expression |
| `plotting.main_plotting_var.define_scalar_expression.expression` | `"expression_here"` | Mathematical expression definition |

### Thresholding

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.main_plotting_var.thresholding.on` | `0` | Enable thresholding (0=off, 1=on) |
| `plotting.main_plotting_var.thresholding.var.name` | `"eta"` | Variable to threshold by |
| `plotting.main_plotting_var.thresholding.var.min` | `0.0` | Minimum threshold value |
| `plotting.main_plotting_var.thresholding.var.max` | `1e37` | Maximum threshold value |

## Background Variable

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.background_var.on` | `0` | Enable background variable (0=off, 1=on) |
| `plotting.background_var.name` | `"eta"` | Background variable name |
| `plotting.background_var.invert` | `0` | Invert background colors (0=off, 1=on) |
| `plotting.background_var.colormap` | `"gray"` | Background colormap |

## Contours

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.contour.on` | `0` | Enable contour lines (0=off, 1=on) |
| `plotting.contour.var.name` | `"phi"` | Variable to contour |
| `plotting.contour.values` | `0.5` | Contour value(s) |
| `plotting.contour.linewidth` | `2` | Contour line width |
| `plotting.contour.color` | `(0, 0, 0, 255)` | Contour color (RGBA) |

## Legend

| Parameter | Default | Description |
|-----------|---------|-------------|
| `plotting.legend.name.on` | `0` | Enable legend (0=off, 1=on) |
| `plotting.legend.name.text` | `"Good Legend"` | Legend text |
| `plotting.legend.name.position.x` | `-1150` | Legend X position |
| `plotting.legend.name.position.y` | `-800` | Legend Y position |
| `plotting.legend.name.dpi` | `500` | Legend resolution (DPI) |
| `plotting.legend.name.fontsize` | `8` | Legend font size |

## Notes

- Boolean parameters use `0` for off/disabled and `1` for on/enabled
- Color values are specified as RGBA tuples with values 0-255
- Use `-1` for `step.end` to process all available timesteps