#!/usr/bin/env python

import os
import sys

def delete_delete_me_files(directory="."):
    import os
    """
    Deletes all files in the given directory whose names contain 'DELETE_ME'.
    Defaults to the current directory.
    """
    deleted = 0

    for filename in os.listdir(directory):
        if "DELETE_ME" in filename:
            filepath = os.path.join(directory, filename)

            if os.path.isfile(filepath):
                os.remove(filepath)
                deleted += 1
    return

ALLOWED_COLORMAPS = {
    "rainbow",
    "viridis",
    "plasma",
    "gray",
    "blues",
    "magma",
    "inferno",
    "cividis",
    "BuGn",
    "Oranges",
    "PuBu",
    "GnBu",
    "Greens",
    "OrRd",
    "PRGn",
    "Dark2",
    "Paired",
    "PiYG",
    "PuBu",
    "PuBuGn",
    "PuOr",
    "PuRd",
    "Purples",
    "RdBu",
    "RdGy",
    "RdPu",
    "RdYlBu",
    "RdYlGn",
    "Reds",
    "Set1",
    "Spectral",
    "YlgGn",
    "YlGnBu",
    "YlOrBr",
    "YlOrRd",
    "turbo",
    "hot",
}

# -----------------------------
# Default parameters
# -----------------------------
DEFAULTS = {
    # Database
    "file.db_path": os.getcwd(), # Path to database directory
    "file.default_db": "celloutput.visit", # Default database filename
    "file.output_filename": "high_var_all_time", # Output file name for generated visualizations
    "file.width": 1080, # Output image width in pixels
    "file.height": 1080, # Output image height in pixels

    # Step control
    "step.interval": 1, # Interval between timesteps
    "step.start": 0, # Starting timestep
    "step.end": -1, # Ending timestep (-1 = all timesteps)

    # Plotting Variables
    "plotting.main_plotting_var.name": "temp", # Variable to plot
    "plotting.main_plotting_var.colormap": "plasma", # Colormap for visualization, see available colormaps section for support VisIt colormaps
    "plotting.main_plotting_var.define_scalar_expression.on": 0, # Enable custom scalar expression (0=off, 1=on)
    "plotting.main_plotting_var.define_scalar_expression.name": "expression_name", # Name for the expression
    "plotting.main_plotting_var.define_scalar_expression.expression": "expression_here", # Mathematical expression definition
    "plotting.main_plotting_var.min": 0, # Minimum value for color scale
    "plotting.main_plotting_var.max": 2000, # Maximum value for color scale

    # Thresholding
    "plotting.main_plotting_var.thresholding.on": 0, # Enable thresholding (0=off, 1=on)
    "plotting.main_plotting_var.thresholding.var.name": "eta", # Variable to threshold by
    "plotting.main_plotting_var.thresholding.var.min": 0.0, # Minimum threshold value
    "plotting.main_plotting_var.thresholding.var.max": 1e37, # Maximum threshold value
    
    # Background variable
    "plotting.background_var.on": 0, # Enable background variable (0=off, 1=on)
    "plotting.background_var.name": "eta", # Background variable name
    "plotting.background_var.invert": 0, # Invert background colors (0=off, 1=on)
    "plotting.background_var.colormap": "gray", # Background colormap

    # Background image
    "plotting.background_img.on": 0, # Enable a background image instead of a background variable
    "plotting.background_img.name": "path/to/img/img.png", # Path to background image

    # Contours
    "plotting.contour.on": 0, # Enable contour lines (0=off, 1=on)
    "plotting.contour.var.name": "phi", # Variable to contour
    "plotting.contour.values": 0.5, # Contour value(s)
    "plotting.contour.linewidth": 2, # Contour line width
    "plotting.contour.color": (0, 0, 0, 255),  # Contour color (RGBA) (default: black)
    
    # Legend
    "plotting.legend.on": 0, # Enable legend (0=off, 1=on)
    "plotting.legend.position": "right", # Legend X position (left/right/top/bottom)
    "plotting.legend.name.on": 0, # Enable legend name/label (0=off, 1=on)
    "plotting.legend.name.text": "Good Legend", # Legend text
    "plotting.legend.name.fontsize": 8, # Legend font size
    "plotting.legend.ticks.numticks": 5, # Number of ticks in the colorbar
    "plotting.legend.ticks.fontsize": 10, # fontsize of the ticks in the colorbar

    # High variable comparsion mode
    "high_var.mode": "space", # The 2 different modes for the high_var.sh script, see the high var section for details, the two options are time and space

    # Data Transfer (): Not meant as inputs, used to transfer data between scripts
    "sim.time.arr": 0, # not a user input, used to transfer data between scripts, will get overwritten if included in input file
}


# -----------------------------
# Read input file
# -----------------------------
def read_input_file(fname):
    """
    Reads a simple key = value input file.
    Ignores empty lines and lines starting with #.
    Auto-converts int, float, bool values.
    Also converts comma-separated numbers into tuples for keys that need it.
    """
    RED = "\033[91m"
    RESET = "\033[0m"

    # Keys that should be interpreted as tuple of floats
    tuple_keys = {"plotting.contour.values"}
    color_keys = {"plotting.contour.color"}

    params = {}
    with open(fname, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                print(f"{RED}WARNING: Skipping malformed line: {line}{RESET}")
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            # Handle tuple-like values for specific keys
            if key in tuple_keys:
                # Split by comma
                if "," in value:
                    parts = value.split(",")
                    vals = []
                    for p in parts:
                        p = p.strip()
                        try:
                            vals.append(float(p))
                        except ValueError:
                            print(f"{RED}WARNING: Could not convert '{p}' to float for key '{key}'. Ignoring.{RESET}")
                    if vals:
                        params[key] = tuple(vals)
                    else:
                        print(f"{RED}WARNING: No valid numbers for key '{key}'. Using default (0.5){RESET}")
                        params[key] = (0.5,)
                else:
                    # Single number
                    try:
                        params[key] = (float(value),)
                    except ValueError:
                        print(f"{RED}WARNING: Could not convert '{value}' to float for key '{key}'. Using default (0.5){RESET}")
                        params[key] = (0.5,)
                continue  # skip the rest of type conversion

            # ... inside the line parsing loop
            if key in color_keys:
                params[key] = parse_rgba(value)
                continue

            # Auto-convert other types
            if value.lower() in ("true", "false"):
                value = value.lower() == "true"
            else:
                try:
                    if "." in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    pass  # keep as string

            params[key] = value

    return params



# -----------------------------
# Merge defaults + input file
# -----------------------------
def get_parameters(input_file=None):
    """
    Returns a dictionary of parameters:
        defaults overridden by input file (if provided)
    """
    params = DEFAULTS.copy()
    inputs = {}

    if input_file:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        inputs = read_input_file(input_file)

    # Warn on unknown keys
    for key in inputs:
        if key not in DEFAULTS:
            RED = "\033[91m"
            RESET = "\033[0m"
            print(f"{RED}WARNING: Unknown input key '{key}'{RESET}")

    params.update(inputs)

    cmap = params["plotting.main_plotting_var.colormap"]
    if cmap not in ALLOWED_COLORMAPS:
        raise ValueError(
            f"Invalid colormap '{params['plotting.main_plotting_var.colormap']}'.\n"
            f"Allowed colormaps are:\n"
            f"{sorted(ALLOWED_COLORMAPS)}"
        )
    
    cmap = params["plotting.background_var.colormap"]
    if cmap not in ALLOWED_COLORMAPS:
        raise ValueError(
            f"Invalid colormap '{params['plotting.background_var.colormap']}'.\n"
            f"Allowed colormaps are:\n"
            f"{sorted(ALLOWED_COLORMAPS)}"
        )

    return params

def write_time(input_file=None, time_arr=None):
    import os

    if input_file is None:
        raise ValueError("input_file must be specified")
    if time_arr is None:
        raise ValueError("time_arr must be specified")
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Read the current file
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Check if a line starts with "sim.time.arr" and replace it
    found = False
    for i, line in enumerate(lines):
        if line.strip().startswith("sim.time.arr"):
            lines[i] = "sim.time.arr = " + ",".join(str(t) for t in time_arr) + "\n"
            found = True
            break

    # If not found, append at the end
    if not found:
        lines.append("sim.time.arr = " + ",".join(str(t) for t in time_arr) + "\n")

    # Write back the whole file
    with open(input_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

def parse_rgba(value_str):
    """
    Parse an RGBA color string like:
        "255, 0, 128, 255"
        "0,0,0,255"
    Returns a tuple of 4 integers.
    """
    RED = "\033[91m"
    RESET = "\033[0m"

    value_str = value_str.split("#")[0].strip()
    value_str = value_str.strip("()")

    parts = value_str.split(",")
    if len(parts) != 4:
        print(f"{RED}WARNING: RGBA value must have 4 components, got {len(parts)}. Using default (0,0,0,255){RESET}")
        return (0, 0, 0, 255)

    rgba = []
    for p in parts:
        try:
            val = int(p.strip())
            if not (0 <= val <= 255):
                raise ValueError
            rgba.append(val)
        except ValueError:
            print(f"{RED}WARNING: Invalid RGBA component '{p}'. Must be 0-255. Using 0.{RESET}")
            rgba.append(0)

    return tuple(rgba)
