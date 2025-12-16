#!/bin/bash

# Usage: ./flame_sfi_script.sh /path/to/input_directory
INPUT_DIR="$1"

# Check if input directory is provided
if [ -z "$INPUT_DIR" ]; then
    echo "Usage: $0 /path/to/input_directory"
    exit 1
fi

# Array of scripts to run
SCRIPTS=(
    "high_stress_all_time.py"
    "high_stress_gif_images.py"
    "initial_phi.py"
    "rel_density_stressXX_gif_images.py"
    "velmag_strainxx_gif_images.py"
)

# Loop through each script and run it with visit
for SCRIPT in "${SCRIPTS[@]}"; do
    echo "Running $SCRIPT on $INPUT_DIR..."
    visit -cli -nowin -np 8 -s "$SCRIPT" "$INPUT_DIR"
done

echo "All scripts completed!"
