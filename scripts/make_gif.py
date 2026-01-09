from PIL import Image
import os

def images_to_gif(image_paths, output_path, fps=10, loop=0):

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

    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=loop,
        optimize=True
    )