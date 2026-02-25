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

        plt.close(fig)
    
    # print(images)

    return images