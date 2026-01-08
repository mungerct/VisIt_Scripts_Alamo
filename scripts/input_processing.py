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

    "plotting.main_plotting_var.thresholding.on": 0,
    "plotting.main_plotting_var.thresholding.var.name": "eta",

    "plotting.background_var.on": 1,
    "plotting.background_var.name": "eta",
    "plotting.background_var.invert": 0,
    "plotting.background_var.colormap": "gray",
    "plotting.legend.name.on": 1,
    "plotting.legend.name.text": "Good Legend",
    "plotting.legend.name.position.x": 10,
    "plotting.legend.name.position.y": 10,
}


# -----------------------------
# Read input file
# -----------------------------
def read_input_file(fname):
    """
    Reads a simple key = value input file.
    Ignores empty lines and lines starting with #.
    Auto-converts int, float, and bool values.
    """
    params = {}
    with open(fname, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                print(f"WARNING: Skipping malformed line: {line}")
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            # Auto-convert types
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
            print(f"WARNING: Unknown input key '{key}'")

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