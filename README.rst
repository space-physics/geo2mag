=======
geo2mag
=======

Convert geodetic coordinates to geomagnetic coordinates, using the `hosted algorithm <http://wdc.kugi.kyoto-u.ac.jp/igrf/gggm/index.html>`_


.. contents::

Install
============
::

    pip install -e .

Usage
=====
This program reads geodetic coordinates from file or command line.

Read coords from file
--------------------------
Convert .KMZ file containing geodetic coordinates to geomagnetic coordinates::

  ./geo2mag.py test/test.kmz

or likewise with a CSV or XLS file.

input coords from terminal
-------------------------------
input geodetic latitude and longitude with the ``-c`` option::

    ./geo2mag.py -c 65 -148
