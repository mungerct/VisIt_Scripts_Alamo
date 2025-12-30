#!/usr/bin/env python
from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt
import sys

def paste_image(background, overlay, position):
    """Paste overlay onto background at the given position using overlay's alpha channel as mask."""
    x, y = position

    overlay_arr = np.array(overlay)
    mask = np.sum(overlay_arr[:, :, :3], axis=2) < 765
    mask_img = Image.fromarray((mask * 255).astype(np.uint8))

    background.paste(overlay, (x, y), mask_img)
    return background

def progress_bar(i, total, width=40):
    frac = i / float(total)
    filled = int(width * frac)
    bar = "#" * filled + "-" * (width - filled)
    sys.stdout.write(
        f"\r  Pasting Images: [{bar}] {i}/{total} ({frac*100:5.1f}%)"
    )
    sys.stdout.flush()
    if i == total:
        print()

def compile_images_func(filename="result_img.png"):

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

    # Collect all existing image filenames first
    filenames = []
    i = 0
    while True:
        filename = f"{basename}{i:04d}{extension}"
        if not os.path.exists(filename):
            break
        filenames.append(filename)
        i += 1

    total = len(filenames)

    # Process images with progress bar
    for idx, filename in enumerate(filenames, start=1):
        img = Image.open(filename).convert("L")
        arr = np.array(img)

        # Keep darker pixels
        result_arr = np.minimum(result_arr, arr)

        # Update progress bar
        progress_bar(idx, total)

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

    result_img = paste_image(result_img, legend, (0, 0))
    result_img = paste_image(result_img, initial_field, (0, 0))

    result_img.save(filename)
    result_img.show()