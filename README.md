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
   visit -cli -nowing -s high_stress_all_time.py /path/to/database

3. (Optional) To run VisIt in parallel with mpi use, replace 8 with your specified number of core
   ```bash
   visit -cli -nowin -np 8 -s high_stress_all_time.py /path/to/database

   Note: The code asuumes your VisIt database is named `celloutput.visit` and you do not need to include this in the file path. i.e. A/B/simulation_folder/ is correct, A/B/simulation_folder/celloutput.visit is wrong

## Parameters
- step_interval = 10         # Change to 5, 10, etc. to skip timesteps
- start_state = 0            # Starting time step index
- end_state = numStates      # Ending time step index (automatically set to total number of states)
- num_levels = 4             # Number of "levels" of the stress that are plotted, more levels will increase fidelity of output
- min_stress_thres = 10      # Minimum stress threshold
- max_stress_thres = 25      # Maximum stress threshold
- invert_phi = 0 # Boolean to invert phi colormap

# VisIt Stress Images for .gif Script (high_stress_gif_images.py)
<details>

## Overview

This script processes simulation data to create visualization frames that can be assembled into animations. It overlays two quantities:
- **Phi field**: Phase field variable (shown in grayscale) visible only where eta (solid phase) > 0.5
- **Von Mises stress**: Stress distribution (color-mapped) shown only above a threshold

## Requirements

- VisIt visualization software
- Simulation output file: `celloutput.visit`
- Python (bundled with VisIt)

## Usage

### Specify Custom Path

Provide the path to the directory containing your data:

```bash
visit -cli -nowin -s visualization_script.py /path/to/simulation/data/
```

## Output

The script creates a directory named after the parent folder of your database and saves PNG frames:

```
output.scp.../
├── phi_highvonMises_gif_frame_0000.png
├── phi_highvonMises_gif_frame_0010.png
├── phi_highvonMises_gif_frame_0020.png
└── ...
```

**Frame specifications:**
- Format: PNG
- Resolution: 2000×2000 pixels
- Naming: Sequential with timestep number
- Background: White

## Configuration

### Adjustable Parameters

Edit these variables in the script to customize output:

```python
# Time range
start_state = 0           # Starting timestep
end_state = 500           # Maximum timestep (capped at total available)
step_interval = 10        # Frame every N timesteps

# Stress thresholds
min_stress_thres = 12.5   # Minimum von Mises stress to display
max_stress_thres = 25     # Maximum for color scale

# Eta threshold for phi display
# (hardcoded to 0.5 in PhiThresh)
```

### Von Mises Stress Expression

The script defines von Mises stress as:

```python
sqrt(stress_xx^2 + stress_yy^2 - stress_xx*stress_yy + 3*stress_xy^2) / 10
```

## Visualization Details

### Layer 1: Phi Field
- **Variable**: `phi`
- **Color scheme**: Grayscale
- **Range**: 0 to 1
- **Visibility**: Only where `eta > 0.5`
- **Purpose**: Shows phase field distribution in the material

### Layer 2: Von Mises Stress
- **Variable**: `stress_von_mesis` (custom expression)
- **Color scheme**: Default VisIt colormap
- **Range**: 0 to 25 (configurable)
- **Visibility**: Only where stress > 12.5 AND `eta > 0.5`
- **Purpose**: Highlights regions of high mechanical stress

```

## Troubleshooting

**Error: "Could not find celloutput.visit"**
- Ensure the database file exists in the specified directory
- Check that the path is correct when using command-line arguments

**No frames generated**
- Verify that your database contains the required variables: `phi`, `eta`, `stress_xx`, `stress_yy`, `stress_xy`
- Check that there are timesteps within your configured range

**Blank or unexpected visualization**
- Adjust threshold values if your data range differs
- Verify that `eta > 0.5` regions exist in your simulation

## Author

[Caleb Munger]
