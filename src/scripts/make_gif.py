from PIL import Image
import os
from .compile_images import crop_image, add_colorbar
import matplotlib.pyplot as plt
import numpy as np

def images_to_gif(image_paths, params, fps, loop=0):

    """
    Create a GIF from a list of image paths.

    Args:
        image_paths (list[str]): Paths to image files (in order).
        output_path (str): Output GIF file path.
        duration (int): Time between frames in milliseconds.
        loop (int): Number of loops (0 = infinite).
    """

    from PIL import Image

    if not image_paths:
        raise ValueError("image_paths list is empty")

    duration = int(1000 / fps)

    images = [Image.open(p).convert("RGBA") for p in image_paths]

    images = process_images(images, params)

    output_path = params["file.output_filename"] + ".gif"
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=loop,
        optimize=True
    )
    print(f"Saved GIF to {output_path} with {len(images)} frames at {fps} FPS")
    return

def images_to_webm(image_paths, params, fps):
    """
    Create a WebM video from a list of image paths.
    Args:
        image_paths (list[str]): Paths to image files (in order).
        params (dict): Parameter dictionary including output filename.
        fps (int): Frames per second.
    """
    import imageio
    import numpy as np
    from PIL import Image

    if not image_paths:
        raise ValueError("image_paths list is empty")

    # Load and process images using your existing pipeline
    images = [Image.open(p).convert("RGB") for p in image_paths]
    images = process_images(images, params)

    output_path = params["file.output_filename"] + ".webm"

    # Convert PIL images to numpy arrays
    frames = [np.array(img) for img in images]
    quality = params["gif_images.webm.quality"]
    # Write frames to WebM
    # imageio.mimwrite(output_path, frames, fps=fps, codec="vp9", format="webm", quality=quality)
    imageio.mimwrite(output_path, frames, fps=fps, codec="vp9", format="webm",
                output_params=["-crf", str(quality), "-b:v", "0"])

    print(f"Saved WebM to {output_path} with {len(images)} frames at {fps} FPS")

def process_images(images, params):

    for k in range(len(images)):
        images[k] = crop_image(images[k])

        fig, ax = plt.subplots(figsize=(8, 8))

        ax.imshow(images[k])
        ax.axis("off")


        if params["gif_images.mode"] != "grid":
            images[k] = add_colorbar(fig, ax, params)
        fig.tight_layout(pad = 0.1)
        fig.canvas.draw()

        # Get width and height
        w, h = fig.canvas.get_width_height()

        # ARGB buffer → array
        buf = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)
        buf = buf.reshape((h, w, 4))

        # Convert ARGB → RGBA
        buf = buf[:, :, [1, 2, 3, 0]]

        # Convert to PIL Image
        images[k] = Image.fromarray(buf, mode="RGBA")

        # Get tight bounding box in inches
        bbox = fig.get_tightbbox(fig.canvas.get_renderer())
        bbox_inches = bbox.transformed(fig.dpi_scale_trans.inverted())

        # Resize figure exactly to bounding box
        fig.set_size_inches(bbox_inches.width, bbox_inches.height)

        # Redraw after resizing
        fig.canvas.draw()

        # size_inches = fig.get_size_inches()
        # print(f"Figure size in inches: {size_inches}")

        # plt.show()
        plt.close(fig)
    
    # print(images)

    return images

def images_to_grid(image_paths, params, cols=9, padding=50):
    from PIL import Image
    import math

    cols = params["gif_images.grid.ncols"]
    padding = params["gif_images.grid.padding"]

    if not image_paths:
        raise ValueError("image_paths list is empty")

    # images = [Image.open(p).convert("RGB") for p in image_paths]
    
    images = []
    for p in image_paths:
        img = Image.open(p).convert("RGB")
        images.append(img)

    images = process_images(images, params)

    for i in range(len(images)):
        images[i] = trim_whitespace(images[i])
        img_w, img_h = images[i].size

    n = len(images)
    rows = math.ceil(n / cols)

    # Assume all images same size
    img_w, img_h = images[0].size

    grid_w = cols * img_w + padding * (cols - 1)
    grid_h = rows * img_h + padding * (rows - 1)

    grid_img = Image.new("RGB", (grid_w, grid_h), color=(255, 255, 255))

    for idx, img in enumerate(images):
        row = idx // cols
        col = idx % cols

        x = col * (img_w + padding)
        y = row * (img_h + padding)

        grid_img.paste(img, (x, y))

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.imshow(grid_img)
    ax.axis("off")

    grid_img = add_colorbar(fig, ax, params)
    fig.tight_layout(pad = 0.1)
    fig.canvas.draw()
    # plt.show()
    output_path = params["file.output_filename"] + ".png"

    plt.savefig(output_path, dpi=600, bbox_inches="tight")
    # grid_img.show()
    # grid_img.save(output_path)

    print(f"Saved grid to {output_path}")


def trim_whitespace(img, threshold=245):
    """
    Remove white borders from an image.
    threshold: pixels above this value are considered white.
    """

    img = img.convert("RGB")
    np_img = np.array(img)

    # Create mask of non-white pixels
    mask = np.any(np_img < threshold, axis=2)

    coords = np.argwhere(mask)

    if coords.size == 0:
        print("Image appears completely white.")
        return img

    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1

    return img.crop((x0, y0, x1, y1))