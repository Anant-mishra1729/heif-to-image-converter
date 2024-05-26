# HEIF to Image Converter

This is a command-line tool to convert HEIF images to other image formats such as JPEG, PNG, etc. It uses pillow-heif to read and convert HEIF images. It also **supports multiprocessing** to speed up the conversion process.

> **Note**
> This converter supports extraction of images from the heic file.

## Installation

* Clone the repository
```bash
git clone https://github.com/Anant-mishra1729/heif-to-image-converter.git
```
* Install the dependencies
```bash
pip install pillow-heif tqdm
```

## Usage

```bash
usage: htoi.py [-h] -i IMAGE [-o OUTPUT] [-t TYPE] [-q QUALITY] [-p PROCESSES]

options:
  -h, --help            show this help message and exit
  -i IMAGE, --image IMAGE
                        Image to convert
  -o OUTPUT, --output OUTPUT
                        Output directory
  -t TYPE, --type TYPE  Type of image: jpg, png etc. (default = jpg)
  -q QUALITY, --quality QUALITY
                        Quality of image (default = 100)
  -p PROCESSES, --processes PROCESSES
                        Number of processes to use (default = 2)
```

## Example

```bash
python htoi.py -i Cyprus.heic -o cyprus -t jpg -q 100 -p 3
```

## Multiprocessing
By default, the script by default uses 2 processes to convert the images. You can change the number of processes using the `-p` option.

## License
[MIT](https://choosealicense.com/licenses/mit/)
