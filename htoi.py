import os
import argparse
import multiprocessing as mp
from tqdm import tqdm
import pillow_heif as ph


def save_images(images, start, output_path, image_type, quality, position=0):
    for i, image in tqdm(
        enumerate(images),
        total=len(images),
        desc=f"Converting {start + 1} to {start + len(images)}",
        position=position,
    ):
        image.save(
            os.path.join(output_path, f"{i + start}.{image_type}"),
            quality=quality,
        )


def convert_heif_to_images(image_path, output_path, image_type, quality, processes):
    heif_file = ph.open_heif(image_path)
    num_images = len(heif_file)
    print(f"\nFound {num_images} images in the HEIF file. Converting...\n")

    images = [image.to_pillow() for image in heif_file]
    chunk_size = (num_images + processes - 1) // processes
    tasks = [
        (images[i:i + chunk_size], i, output_path, image_type, quality)
        for i in range(0, num_images, chunk_size)
    ]
    with mp.Pool(processes) as pool:
        pool.starmap(save_images, tasks)
    print("\nImages saved to", os.path.abspath(output_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", help="Image to convert", required=True)
    parser.add_argument("-o", "--output", help="Output directory", default="")
    parser.add_argument(
        "-t", "--type", help="Type of image: jpg, png etc. (default = jpg)", default="jpg"
    )
    parser.add_argument(
        "-q",
        "--quality",
        help="Quality of image (default = 100)", 
        default=100, 
        type=int,
    )
    parser.add_argument(
        "-p",
        "--processes", 
        help="Number of processes to use (default = 2)", 
        default=2, 
        type=int,
    )

    args = parser.parse_args()

    if not os.path.exists(args.image):
        print("Image not found")
        exit(1)

    output_path = args.output or args.image.split(".")[0]
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    else:
        print("Output directory already exists. Do you want to overwrite the images?")
        choice = input("(y/n): ")
        if choice.lower() != "y":
            print("Exiting...")
            exit(1)

    convert_heif_to_images(args.image, output_path, args.type, args.quality, args.processes)
