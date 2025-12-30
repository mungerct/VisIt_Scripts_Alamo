#!/usr/bin/env python
from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt

def paste_image(background, overlay, position):
    """Paste overlay onto background at the given position using overlay's alpha channel as mask."""
    x, y = position

    overlay_arr = np.array(overlay)
    mask = np.sum(overlay_arr[:, :, :3], axis=2) < 765
    mask_img = Image.fromarray((mask * 255).astype(np.uint8))

    background.paste(overlay, (x, y), mask_img)
    return background

basename = "temp_field_DELETE_ME"
extension = ".png"
start = 0
legend = Image.open("legend_only_DELETE_ME0000.png").convert("RGBA")
initial_field = Image.open("initial_field_DELETE_ME0000.png").convert("RGBA")

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

# # Create mask: True where legend is NOT white
# legend_arr = np.array(legend)
# # Sum RGB channels; white = 255+255+255 = 765
# mask = np.sum(legend_arr[:, :, :3], axis=2) < 765

# # Convert mask to 8-bit alpha channel (0=transparent, 255=opaque)
# mask_img = Image.fromarray((mask * 255).astype(np.uint8))

# # Position: top-right corner
# x = 0
# y = 0

# # Paste using mask
# result_img.paste(legend, (x, y), mask_img)

# Save result

result_img = paste_image(result_img, legend, (0, 0))
result_img = paste_image(result_img, initial_field, (0, 0))

result_img.save("finished_image.png")
result_img.show()