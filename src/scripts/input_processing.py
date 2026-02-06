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
    "file.db_path": os.getcwd(),
    "file.default_db": "celloutput.visit",
    "file.output_filename": "high_var_all_time",
    "file.width": 1080,
    "file.height": 1080,

    # Step control
    "step.interval": 1,
    "step.start": 0, 
    "step.end": -1, # -1 means all available timesteps

    # Plotting Variables
    "plotting.main_plotting_var.name": "temp",
    "plotting.main_plotting_var.colormap": "plasma",
    "plotting.main_plotting_var.define_scalar_expression.on": 0,
    "plotting.main_plotting_var.define_scalar_expression.name": "expression_name",
    "plotting.main_plotting_var.define_scalar_expression.expression": "expression_here",
    "plotting.main_plotting_var.min": 0,
    "plotting.main_plotting_var.max": 2000,

    # Thresholding
    "plotting.main_plotting_var.thresholding.on": 0,
    "plotting.main_plotting_var.thresholding.var.name": "eta",
    "plotting.main_plotting_var.thresholding.var.min": 0.0,
    "plotting.main_plotting_var.thresholding.var.max": 1e37,
    
    # Background variable
    "plotting.background_var.on": 0,
    "plotting.background_var.name": "eta",
    "plotting.background_var.invert": 0,
    "plotting.background_var.colormap": "gray",

    # Contours
    "plotting.contour.on": 0,
    "plotting.contour.var.name": "phi",
    "plotting.contour.values": 0.5,
    "plotting.contour.linewidth": 2,
    "plotting.contour.color": (0, 0, 0, 255),  # black
    
    # Legend
    "plotting.legend.on": 0,
    "plotting.legend.position": "right",
    "plotting.legend.name.on": 0,
    "plotting.legend.name.text": "Good Legend",
    "plotting.legend.name.fontsize": 8,
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
