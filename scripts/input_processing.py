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

# -----------------------------
# Default parameters
# -----------------------------
DEFAULTS = {
    # Database
    "db_path": os.getcwd(),
    "default_db": "celloutput.visit",
    "output_filename": "high_var_all_time",

    # Step control
    "step.interval": 1,
    "step.start": 0, 
    "step.end": -1, # -1 means all available timesteps

    # Variable control
    "var.min": 1200,
    "var.max": 2000,

    # Variables
    "main_plotting_var": "temp",
    "background_var": "eta",
    "invert_phi": 0,
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
    return params