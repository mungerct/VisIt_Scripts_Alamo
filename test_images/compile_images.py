#!/usr/bin/env python
from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt

basename = "temp_field_DELETE_ME"
extension = ".png"
start = 0

# Open first image to initialize result
filename = f"{basename}{start:04d}{extension}"
result_img = Image.open(filename).convert("L")
result_arr = np.array(result_img)

i = start + 1

while True:
    filename = f"{basename}{i:04d}{extension}"

    if not os.path.exists(filename):
        break

    img = Image.open(filename).convert("L")
    arr = np.array(img)

    # Keep darker pixels
    result_arr = np.minimum(result_arr, arr)

    i += 1

# Create mask: True where pixel is NOT white
mask = result_arr < 255

# Normalize grayscale for colormap
norm = result_arr / 255.0

# Apply plasma colormap
plasma = plt.cm.plasma(norm)[:, :, :3]  # RGB only

# Convert to uint8
plasma_rgb = (plasma * 255).astype(np.uint8)

# Start with a white RGB image
result = np.ones((*result_arr.shape, 3), dtype=np.uint8) * 255

# Replace only non-white pixels
result[mask] = plasma_rgb[mask]

# Convert to image
result_img = Image.fromarray(result)

# Show / save
result_img.show()