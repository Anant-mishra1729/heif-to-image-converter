import pyheif
from PIL import Image
import tqdm
import argparse
import os
import multiprocessing as mp


class Converter:
    def __init__(self, image_path, output_path):
        self.images = pyheif.open_container(image_path).top_level_images
        self.output_path = output_path

    def convert(self, image_type="jpg", quality=100):
        # Use tqdm to show progress bar
        for i, undecoded_image in tqdm.tqdm(
            enumerate(self.images),
            total=len(self.images),
            desc=f"Converting to {image_type}",
        ):
            heif_file = undecoded_image.image.load()
            image = Image.frombytes(
                mode=heif_file.mode,
                size=heif_file.size,
                data=heif_file.data,
                decoder_name="raw",
            )
            image.save(
                os.path.join(self.output_path, f"{i}.{image_type}"), quality=quality
            )
            del image
            del heif_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", help="Image to convert", required=True)
    parser.add_argument("-o", "--output", help="Output directory")
    parser.add_argument(
        "-t", "--type", help="Type of image (jpg, png etc.)", default="jpg"
    )
    parser.add_argument(
        "-q",
        "--quality",
        help="Quality of image (default = 100)",
        default=100,
        type=int,
    )
    args = parser.parse_args()

    if not os.path.exists(args.image):
        print("Image not found")
        exit(1)

    if not args.output:
        # Make directory with the name of image
        os.mkdir(args.image.split(".")[0])
        args.output = args.image.split(".")[0]
    else:
        if not os.path.exists(args.output):
            os.mkdir(args.output)

    converter = Converter(args.image, args.output)
    converter.convert(args.type, args.quality)
