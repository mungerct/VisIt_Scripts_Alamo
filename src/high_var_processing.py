#!/usr/bin/env python

import sys
import os
from scripts.input_processing import delete_delete_me_files, get_parameters
from scripts.compile_images import compile_images_func

input_file = sys.argv[1] if len(sys.argv) > 1 else None
params = get_parameters(input_file)

compile_images_func(
    basename="temp_field_DELETE_ME",
    extension=".png",
    legend_file="legend_only_DELETE_ME0000.png",
    initial_field_file="initial_field_DELETE_ME0000.png",
    contour_field="contour_field_DELETE_ME0000.png",
    output_file=params["file.output_filename"] + ".png",
    params=params,
)

delete_delete_me_files()