[![Build Status](https://travis-ci.org/scivision/igrfcoord.svg?branch=master)](https://travis-ci.org/scivision/igrfcoord)
[![Coverage Status](https://coveralls.io/repos/github/scivision/igrfcoord/badge.svg?branch=master)](https://coveralls.io/github/scivision/igrfcoord?branch=master)

# Geographic &harr; Geomagnetic Coordinate Conversion

Convert geodetic coordinates to geomagnetic coordinates, using the UNENCRYPTED
connection to IGRF web service:
http://wdc.kugi.kyoto-u.ac.jp/igrf/gggm/index.html

## Install

```sh
python -m pip install -e .
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

    ./geo2mag.py 2017 -f test/test.kmz

or likewise with a CSV or XLS file.


