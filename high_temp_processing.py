#!/usr/bin/env python

import sys
import os
from scripts.input_processing import delete_delete_me_files
from scripts.compile_images import compile_images_func
from scripts.input_processing import get_parameters


input_file = sys.argv[1] if len(sys.argv) > 1 else None
params = get_parameters(input_file)

# Default database filename
default_db = "initial_field_DELETE_ME0000.png"

image_dir = params["file.db_path"]

# # ------------------------------------------------------------
# # Database / working directory handling
# # ------------------------------------------------------------
# if len(sys.argv) > 1:
#     # The first argument is the folder containing the images
#     image_dir = sys.argv[1]
# else:
#     image_dir = os.getcwd()  # fallback to current directory

# Make it absolute and check it exists
image_dir = os.path.abspath(image_dir)
if not os.path.isdir(image_dir):
    raise NotADirectoryError(f"{image_dir} is not a valid directory")

# # Change current working directory to the image directory
# os.chdir(image_dir)
# print(f"Changed working directory to: {image_dir}")

# # Construct full path to the default database
db_path = os.path.join(image_dir, default_db)

# Optional: warn if the database file is missing
if not os.path.exists(db_path):
    print(f"Warning: {default_db} not found in {image_dir}")

# ------------------------------------------------------------
# Output directory
# ------------------------------------------------------------
# parent_dir = os.path.dirname(db_path)
# folder_name = os.path.basename(parent_dir)
# output_dir = os.path.join(os.getcwd(), folder_name)

compile_images_func(
    basename="temp_field_DELETE_ME",
    extension=".png",
    legend_file="legend_only_DELETE_ME0000.png",
    initial_field_file="initial_field_DELETE_ME0000.png",
    output_file="result_img.png"
)
delete_delete_me_files()