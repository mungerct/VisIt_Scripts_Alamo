#!/usr/bin/env python

def compile_images_func(
    basename="temp_field_DELETE_ME",
    extension=".png",
    legend_file="legend_only_DELETE_ME0000.png",
    initial_field_file="initial_field_DELETE_ME0000.png",
    contour_field="contour_field_DELETE_ME0000.png",
    output_file="result_img.png",
    params = None,
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
    
    if params["high_var.mode"] == "time":
        total = len(filenames)
        cmap = get_colormap(params["plotting.main_plotting_var.colormap"])  # first = yellow
        norm_indices = np.linspace(0, 1, total)

        composite_arr = None  # to hold the growing composite

        for idx, filename in enumerate(filenames):
            # Load image in grayscale
            img = Image.open(filename).convert("L")
            arr = np.array(img)

            # Map current index to a color
            color = cmap(norm_indices[idx])[:3]  # RGB values (0-1)

            # Create RGB array for this image (non-white pixels get colormap color)
            rgb_arr = np.ones((arr.shape[0], arr.shape[1], 3))  # start with white
            mask = arr < 255
            rgb_arr[mask] = color

            # Initialize composite if first image
            if composite_arr is None:
                composite_arr = rgb_arr
            else:
                # Paste current image over composite, only where non-white
                composite_arr[mask] = rgb_arr[mask]

            composite_uint8 = (composite_arr * 255).astype(np.uint8)
            result_img = Image.fromarray(composite_uint8)

            progress_bar(idx + 1, total, width=40)

        print("Done creating composite")

    if params["high_var.mode"] == "space":
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

        # Apply colormap
        mask = result_arr < 255
        norm = result_arr / 255.0
        cmap = get_colormap(params["plotting.main_plotting_var.colormap"])
        cmap = cmap.reversed()
        colormap_rgb = cmap(norm)[:, :, :3]
        colormap_rgb = (colormap_rgb * 255).astype(np.uint8)

        result = np.ones((*result_arr.shape, 3), dtype=np.uint8) * 255
        result[mask] = colormap_rgb[mask]
        result_img = Image.fromarray(result)

    if params["plotting.background_var.on"]:
        initial_field_path = os.path.join(cwd, initial_field_file)
        initial_field = Image.open(initial_field_path).convert("RGBA")
        result_img = paste_image(initial_field, result_img, position=(0, 0))

    if params["plotting.contour.on"]:
        contour_path = os.path.join(cwd, contour_field)
        contour_field = Image.open(contour_path).convert("RGBA")
        result_img = paste_image(result_img, contour_field, position=(0,0))

    fig, ax = plt.subplots(figsize=(6, 6))

    cropped_np = crop_image(result_img)

    ax.imshow(cropped_np)
    ax.axis("off")

    fig = add_colorbar(fig, ax, params, cwd)
    # fig.show()
    # input("Press Enter to continue...")

    fig.savefig(os.path.join(cwd, params["file.output_filename"] + ".png"), dpi=800, bbox_inches="tight", pad_inches=0)


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

def latex_text_image(
    text,
    fontsize=12,
    dpi=400,
    color="black",
):
    import matplotlib.pyplot as plt
    import numpy as np
    from PIL import Image
    from io import BytesIO

    fig = plt.figure()
    fig.patch.set_alpha(0)

    # Render text
    plt.text(
        0.5, 0.5, text,
        fontsize=fontsize,
        color=color,
        ha="center",
        va="center",
    )
    plt.axis("off")

    # Save to buffer
    buf = BytesIO()
    plt.savefig(
        buf,
        format="png",
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0.01,
        transparent=True,
    )
    plt.close(fig)

    buf.seek(0)
    return Image.open(buf).convert("RGBA")

def add_colorbar(fig, ax, params, cwd):
    import matplotlib as mpl
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    """
    Adds a configurable colorbar (left/right/top/bottom) using make_axes_locatable
    and saves the figure.
    """

    if params["plotting.legend.on"]:
        if params["high_var.mode"] == "space":
            vmin = params["plotting.main_plotting_var.min"]
            vmax = params["plotting.main_plotting_var.max"]
        
        if params["high_var.mode"] == "time":
            vmin = params["sim.time.start"]
            vmax = params["sim.time.end"]

        cmap = get_colormap(params["plotting.main_plotting_var.colormap"])
        position = params["plotting.legend.position"]

        # ScalarMappable only for the colorbar
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
        sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
        sm.set_array([])

        divider = make_axes_locatable(ax)

        # ---- CREATE COLORBAR AXES OUTSIDE IMAGE ----
        if position == "right":
            cax = divider.append_axes("right", size="4%", pad=0.08)
            cbar = fig.colorbar(sm, cax=cax, orientation="vertical")

        elif position == "left":
            cax = divider.append_axes("left", size="4%", pad=0.75)
            cbar = fig.colorbar(sm, cax=cax, orientation="vertical")

        elif position == "top":
            cax = divider.append_axes("top", size="6%", pad=0.35)
            cbar = fig.colorbar(sm, cax=cax, orientation="horizontal")
            cbar.ax.xaxis.set_label_position("top")
            cbar.ax.xaxis.tick_top()

        elif position == "bottom":
            cax = divider.append_axes("bottom", size="6%", pad=0.35)
            cbar = fig.colorbar(sm, cax=cax, orientation="horizontal")

        else:
            raise ValueError(
                f"Invalid legend position '{position}'. "
                "Use: left, right, top, bottom."
            )

        # ---- LABEL (also outside image) ----
        if params["plotting.legend.name.on"]:
            cbar.set_label(
                params["plotting.legend.name.text"],
                labelpad=8
            )

        return fig

def crop_image(img):
    from PIL import Image
    import numpy as np
    size_plot = Image.open("size_plot_DELETE_ME0000.png").convert("RGBA")

    # Convert to numpy array
    arr = np.array(size_plot)

    # Create mask of non-white pixels (ignore alpha channel)
    non_white_mask = np.any(arr[:, :, :3] != 255, axis=2)

    # Get bounding box of non-white pixels
    coords = np.column_stack(np.where(non_white_mask))
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)

    # Crop (note: PIL uses (left, upper, right, lower))
    cropped = img.crop((x_min, y_min, x_max + 1, y_max + 1))

    # Convert PIL image → numpy array
    cropped_np = np.array(cropped)

    return cropped_np

if __name__ == "__main__":
    compile_images_func()