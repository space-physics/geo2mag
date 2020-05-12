# Geographic &harr; Geomagnetic Coordinate Conversion

[![Build Status](https://travis-ci.org/space-physics/igrfcoord.svg?branch=master)](https://travis-ci.org/space-physics/igrfcoord)

Convert geodetic coordinates to geomagnetic coordinates, using the UNENCRYPTED
connection to IGRF web service:
http://wdc.kugi.kyoto-u.ac.jp/igrf/gggm/index.html

## Install

```sh
python -m pip install -e .
```

Optional: If you wish to plot maps, consider installing CartoPy like:

```sh
conda install cartopy
```

## Usage

This program reads coordinates from file or command line.

```sh
python GeomagConvert.py 2015 -c 65 -148 geomag
```

> 65.56 -96.46

```sh
python GeomagConvert.py 2015 -c 65.56 -96.46 geodetic
```

> 65.004 -147.994

### Read coords from file

Convert .KMZ file containing geodetic coordinates to geomagnetic
coordinates:

```sh
python GeomagConvert.py 2015 -f tests/example.kml
```

or likewise with a CSV or XLS file.
