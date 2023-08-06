import sys
import fire
from txt2img.core import core, save_images, show_images
from PIL import TiffTags
import sys

def save(
    *args,
    batch_size: int = 1,
    guidance_scale: float = 3.0,
    upsample_temp: float = 0.997,
):
    """Save image.

    Args:
      *args:
      batch_size: int:  (Default value = 1)
      guidance_scale: float:  (Default value = 3.0)
      upsample_temp: float:  (Default value = 0.997)

    Returns:

    """

    if len(args) > 1:
        prompt = " ".join(args)
    else:
        prompt = args[0]

    tf_img = core(prompt, batch_size, guidance_scale, upsample_temp)
    out_path = prompt.replace(" ", "_") + ".png"
    save_images(tf_img, out_path)


def show_me(
    prompt,
    batch_size: int = 1,
    guidance_scale: float = 3.0,
    upsample_temp: float = 0.997,
):
    """Display image in jupyter notebook.

    Args:
      prompt:
      batch_size: int:  (Default value = 1)
      guidance_scale: float:  (Default value = 3.0)
      upsample_temp: float:  (Default value = 0.997)

    """

    tf_img = core(prompt, batch_size, guidance_scale, upsample_temp)
    show_images(tf_img)

# function alias
show_a = show_me
show = show_me


def cli():
    """ """
    fire.Fire(save)
