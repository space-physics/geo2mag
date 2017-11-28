=======
geo2mag
=======

Convert geodetic coordinates to geomagnetic coordinates, using the
`hosted algorithm <http://wdc.kugi.kyoto-u.ac.jp/igrf/gggm/index.html>`_


.. contents::

Setup
=====

Prereqs
-------
These are only necessary if you want beautiful map plots.

* Mac: `brew install gdal`
* Linux: `apt install libproj-dev`

Install
-------
::

    pip install -e .

Usage
=====
This program reads geodetic coordinates from file or command line.

Read coords from file
--------------------------
Convert .KMZ file containing geodetic coordinates to geomagnetic coordinates::

  ./geo2mag.py 2017 -f test/test.kmz

or likewise with a CSV or XLS file.

input coords from terminal
-------------------------------
input geodetic latitude and longitude directly::

    ./geo2mag.py 2017 65 -148
