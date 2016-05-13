=======
geo2mag
=======

Convert geodetic coordinates to geomagnetic coordinates, using the `hosted algorithm <http://wdc.kugi.kyoto-u.ac.jp/igrf/gggm/index.html>`_


Installation
============
::

    python setup.py develop

Usage
=====
This program can read geodetic coordinates from a file or from the command line.

Read coordinates from file
--------------------------
Convert .KMZ file containing geodetic coordinates to geomagnetic coordinates::

  ./geo2mag.py test/test.kmz

or likewise with a CSV or XLS file.

input coordinates from terminal
-------------------------------
input geodetic latitude and longitude with the -c option::

    ./geo2mag.py -c 65 -148
