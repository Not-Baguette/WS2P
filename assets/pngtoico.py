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
    parser = argparse.ArgumentParser(description='Convert PNG to ICO.')
    parser.add_argument('png_path', type=str, help='Path to the PNG file.')
    parser.add_argument('--ico_path', type=str, help='Path to save the ICO file. If not provided, the PNG file name will be used with the .ico extension.')
    parser.add_argument('--size', type=int, nargs=2, default=[180, 180], help='Size of the ICO file. Default is 180x180.')

    args = parser.parse_args()

    png_to_ico(args.png_path, args.ico_path, tuple(args.size))

if __name__ == "__main__":
    main()