import argparse
import multiprocessing as mp
import os
import pyheif
from PIL import Image
import tqdm


class Converter:
    def __init__(self, image_path, output_path, image_type="jpg", quality=100):
        self.undecoded_images = pyheif.open_container(image_path).top_level_images
        self.output_path = output_path
        self.image_type = image_type
        self.quality = quality

    def convert(self):
        if len(self.undecoded_images) > 1:
            chunks = [
                self.undecoded_images[: len(self.undecoded_images) // 2],
                self.undecoded_images[len(self.undecoded_images) // 2 :],
            ]

            p1 = mp.Process(target=self._convert, args=(chunks[0], 0, 0))
            p2 = mp.Process(
                target=self._convert,
                args=(chunks[1], len(self.undecoded_images) // 2, 1),
            )

            p1.start()
            p2.start()

            p1.join()
            p2.join()
        else:
            self._convert(self.undecoded_images, (0, 1))

        print("\nImages saved to", self.output_path)

    @staticmethod
    def _convert(images, start, position=0):
        for i, undecoded_image in tqdm.tqdm(
            enumerate(images),
            total=len(images),
            desc=f"Converting {start} to {start + len(images)}",
            position=position,
        ):
            heif_file = undecoded_image.image.load()
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )
            image.save(
                os.path.join(args.output, f"{i + start}.{args.type}"),
                quality=args.quality,
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

    converter = Converter(args.image, args.output, args.type, args.quality)
    converter.convert()
