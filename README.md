# HEIF to Image Converter

This is a command-line tool to convert HEIF images to other image formats such as JPEG, PNG, etc. It uses the **pyheif** and **Pillow** libraries to read and convert HEIF images. It also **supports multiprocessing** to speed up the conversion process.

## Installation

* Clone the repository
```bash
git clone https://github.com/Anant-mishra1729/heif-to-image-converter.git
```
* Install the dependencies
```bash
pip install -r requirements.txt
```

## Usage

```bash
usage: htoi_mp.py [-h] -i IMAGE [-o OUTPUT] [-t TYPE] [-q QUALITY]

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE, --image IMAGE
                        Image to convert
  -o OUTPUT, --output OUTPUT
                        Output directory
  -t TYPE, --type TYPE  Type of image (jpg, png etc.)
  -q QUALITY, --quality QUALITY
                        Quality of image (default = 100)
```

## Example

```bash
python htoi_mp.py -i fuji.heic -o fuji -t jpg -q 100
```

## Multiprocessing
By default, the script uses two processes to convert images. This can be modified by changing the number of processes in the script. However, keep in mind that using too many processes may slow down the conversion process due to I/O and memory constraints.


## License
[MIT](https://choosealicense.com/licenses/mit/)