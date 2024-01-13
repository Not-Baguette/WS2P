import argparse
import os
from PIL import Image

def png_to_ico(png_path, ico_path=None, size=(180,180)):
    img = Image.open(png_path)
    img = img.resize(size, Image.LANCZOS)
    if ico_path is None:
        base_name = os.path.splitext(png_path)[0]
        ico_path = base_name + '.ico'
    img.save(ico_path, format='ICO')

def main():
    pngs = [f for f in os.listdir() if f.endswith('.png')]
    for png in pngs:
        png_to_ico(png)

if __name__ == "__main__":
    main()

