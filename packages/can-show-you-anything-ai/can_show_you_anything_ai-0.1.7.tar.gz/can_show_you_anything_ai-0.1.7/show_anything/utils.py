"""A collection of aws tools"""
import os

import fire


def reloat_pillow():
    modules = sys.modules.copy()
    for name, module in modules.items():
      if 'PIL' in name or 'image' in name:
        try:
          reload(module)
        except:
          pass

def check_pillow_import():
    from PIL.TiffTags import IFD
    




if __name__ == "__main__":
    fire.Fire(format_code)
