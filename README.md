# Suspended sediment concentration of glacial stream prototype

This test script attempts to do the following:

- Normalize a set of pictures according to [rg chromaticity](https://en.wikipedia.org/wiki/Rg_chromaticity)
- Select three areas of each picture, using pre-selected coordinates as reference points for white/red/black areas of the reference disc
- Take the pixel-wise average of these areas for the normalized red/green channels, resulting in a single-point "representative pixel value" of each area, and append this to a list
- For each area, take the average of the list of the above pixel-wise average values (mean of means), as well as the standard deviation

### Dependencies

1. [opencv](https://opencv-python-tutroals.readthedocs.org/en/latest/)
2. [numpy](http://www.numpy.org/)
3. [xlsxwriter](https://xlsxwriter.readthedocs.org/)

### Installation

This tutorial assumes you are working in a Linux-like environment
It is best to set up a [virtual environment](https://virtualenv.pypa.io/en/latest/) for installing opencv and numpy

`virtualenv ~/envs/sediments`

Accessing the virtual environment

`source ~/envs/sediments/bin/activate`

Install numpy and xlsxwriter through pip

`pip install numpy`
`pip install xlsxwriter`

I found that the simplest way to get opencv2 going is with a homebrew installation and a symlink. See [this](http://www.mobileway.net/2015/02/14/install-opencv-for-python-on-mac-os-x/) for more details

### Running the script

The script assumes that the images are:

1. in a folder called "sample"
2. are prefixed with 'IMG_' 
3. end with the extension '.CR2'
4. are consecutive in numbering, as this is natural for periodically taken pictures

If no arguments are provided, it will assume a hard-coded starting image '1717' and ending image '1748'. Otherwise, you can provide three arguments:

1. Number of starting image
2. Number of ending image
3. Whether to normalize the pictures (y for true, any other value for false)

For example, running with 'IMG_100.CR2' to 'IMG_120.CR2', with normalization

`python earth.py 100 120 y`