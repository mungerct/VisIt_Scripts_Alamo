#!/usr/bin/env python

import sys
import os
from scripts.input_processing import delete_delete_me_files
from scripts.make_gif import images_to_gif
from scripts.input_processing import get_parameters
from pathlib import Path

input_file = sys.argv[1] if len(sys.argv) > 1 else None
params = get_parameters(input_file)

# Filename pattern
image_pattern = "temp_field_DELETE_ME*.png"

# Get directory from params
image_dir = Path(params["file.db_path"]).expanduser().resolve()

# Check directory exists
if not image_dir.is_dir():
    raise NotADirectoryError(f"{image_dir} is not a valid directory")

# Get a sorted list of matching images
image_list = sorted(image_dir.glob(image_pattern))

# Optional warning if no images are found
if not image_list:
    print(f"Warning: No files matching '{image_pattern}' found in {image_dir}")

images_to_gif(image_list, params, fps=10, loop=0)
delete_delete_me_files()