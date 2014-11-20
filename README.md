infinityfs
==========

Create an virtual "infinite" filesystem on linux using python.

## Install

1. Install [FUSE](http://fuse.sourceforge.net/) with:
`apt-get install fuse`
or
`pacman -S fuse`

2. Download the source at [fusepy](https://github.com/terencehonles/fusepy) and install it using 
`python setup.py install` in the downloaded folder.

3. Download the [code](/infinityfs.py) and run it:
`python infinityfs.py /path/to/mount/point`

## Comments
Please read the [GNU GPL](/LICENSE) before downloading my code.

Do not add any sensitive data to the script as this can be read in the virtual filesystem.
