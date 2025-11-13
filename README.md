# VisIt Stress Visualization Script (high_stress_all_time.py)
<details>
  
## Overview
This Python script automates the visualization of von Mises stress evolution across all time steps using VisIt. It overlays filtered stress plots on a background scalar field (`phi`) and generates a composite image showing stress progression with threshold filtering.

## Purpose
- Visualize von Mises stress across multiple time steps.
- Apply threshold filters to isolate stress levels.
- Overlay stress plots on a grayscale background field.
- Save a composite image with a legend for publication or analysis.

## Requirements
- VisIt installed with Python scripting support.
- NumPy library.
- Access to a valid VisIt-compatible database (e.g., `.visit` file).

## Usage
1. Update the `OpenDatabase` path to point to your `.visit` file.
2. Run the script using VisIt's Python interpreter:
   ```bash
   visit -cli -s -nowin high_stress_all_time.py

## Parameters
- step_interval = 10         # Change to 5, 10, etc. to skip timesteps
- start_state = 0            # Starting time step index
- end_state = numStates      # Ending time step index (automatically set to total number of states)
- num_levels = 4             # Number of "levels" of the stress that are plotted, more levels will increase fidelity of output
- min_stress_thres = 10      # Minimum stress threshold
- max_stress_thres = 25      # Maximum stress threshold
- invert_phi = 0 # Boolean to invert phi colormap
