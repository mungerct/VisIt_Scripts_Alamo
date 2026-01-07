#!/usr/bin/env python

def compile_images_func(
    basename="temp_field_DELETE_ME",
    extension=".png",
    legend_file="legend_only_DELETE_ME0000.png",
    initial_field_file="initial_field_DELETE_ME0000.png",
    output_file="result_img.png",
    colormap="plasma"
):
    """
    Compile a series of images into a single result image with colormap and overlays.
    """
    import os
    from PIL import Image
    import numpy as np
    import matplotlib.pyplot as plt

    # Use current working directory (which you changed to the image folder)
    cwd = os.getcwd()

    legend_path = os.path.join(cwd, legend_file)
    initial_field_path = os.path.join(cwd, initial_field_file)

    # Open overlay images
    legend = Image.open(legend_path).convert("RGBA")
    initial_field = Image.open(initial_field_path).convert("RGBA")

    # Collect all image filenames in cwd
    filenames = []
    i = 0
    while True:
        filename = f"{basename}{i:04d}{extension}"
        full_path = os.path.join(cwd, filename)
        if not os.path.exists(full_path):
            break
        filenames.append(full_path)
        i += 1

    if not filenames:
        raise FileNotFoundError(f"No images found matching {basename}*{extension} in {cwd}")

    # Open first image to initialize result
    result_img = Image.open(filenames[0]).convert("L")
    result_arr = np.array(result_img)

    total = len(filenames)
    for idx, filename in enumerate(filenames, start=1):
        img = Image.open(filename).convert("L")
        arr = np.array(img)
        result_arr = np.minimum(result_arr, arr)
        # update progress bar
        progress_bar(idx, total, width=40)
    print()

    temp_img = Image.fromarray(result)
    temp_img.save("temp_min_image.png")

    # Apply colormap
    mask = result_arr < 255
    norm = result_arr / 255.0
    cmap = get_colormap(colormap)
    colormap_rgb = cmap(norm)[:, :, :3]
    # colormap = plt.cm.get_cmap(colormap)(norm)[:, :, :3]
    colormap_rgb = (colormap_rgb * 255).astype(np.uint8)

    result = np.ones((*result_arr.shape, 3), dtype=np.uint8) * 255
    result[mask] = colormap_rgb[mask]
    result_img = Image.fromarray(result)

    result_img = paste_image(result_img, legend, position=(0, 0))
    result_img = paste_image(result_img, initial_field, position=(0, 0))

    # Save result
    result_img.save(os.path.join(cwd, output_file))
    # result_img.show()


def paste_image(background, overlay, position):
    from PIL import Image
    import numpy as np
    """Paste overlay onto background at the given position using overlay's alpha channel as mask."""
    x, y = position

    overlay_arr = np.array(overlay)
    mask = np.sum(overlay_arr[:, :, :3], axis=2) < 765
    mask_img = Image.fromarray((mask * 255).astype(np.uint8))

    background.paste(overlay, (x, y), mask_img)
    return background

def progress_bar(i, total, width=40):
    import sys
    frac = i / float(total)
    filled = int(width * frac)
    bar = "#" * filled + "-" * (width - filled)
    sys.stdout.write(
        f"\r  Pasting Images: [{bar}] {i}/{total} ({frac*100:5.1f}%)"
    )
    sys.stdout.flush()
    if i == total:
        print()

    return

def hot(N=256):
    from matplotlib.colors import LinearSegmentedColormap
    colors = [
        (0.0, 0.0, 1.0),
        (0.0, 1.0, 1.0),
        (0.0, 1.0, 0.0),
        (1.0, 1.0, 0.0),
        (1.0, 0.0, 0.0),
    ]
    return LinearSegmentedColormap.from_list(
        "hot", colors, N=N
    )

CUSTOM_COLORMAPS = {
    "hot": hot,
}

def get_colormap(name, N=256):
    import matplotlib.pyplot as plt
    if name in CUSTOM_COLORMAPS:
        return CUSTOM_COLORMAPS[name](N)
    else:
        return plt.cm.get_cmap(name, N)

if __name__ == "__main__":
    compile_images_func()