#!/usr/bin/env bash

# Exit immediately if any command fails
# set -e

# -------- User-configurable variables --------
NP=8
VISIT_SCRIPT=~/research/visit_scripts/src/high_var_all_time.py
POST_SCRIPT=~/research/visit_scripts/src/high_var_processing.py
CONDA_ENV=image_processing
# --------------------------------------------

# Check input
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input.txt>"
    exit 1
fi

DATA_DIR="$1"

# conda init > /dev/null 2>&1

echo "Running VisIt CLI script on ${DATA_DIR}..."
visit -cli -np ${NP} -nowin -s "${VISIT_SCRIPT}" "${DATA_DIR}"

# echo "Activating conda environment: ${CONDA_ENV}"
# source "$(conda info --base)/etc/profile.d/conda.sh"
# conda activate "${CONDA_ENV}"

echo "Compiling Images ${DATA_DIR}..."
python "${POST_SCRIPT}" "${DATA_DIR}"

# conda deactivate > /dev/null 2>&1

echo "All steps completed successfully."
