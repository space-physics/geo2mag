.. image:: https://travis-ci.org/scivision/geo2mag.svg?branch=master
    :target: https://travis-ci.org/scivision/geo2mag
.. image:: https://coveralls.io/repos/github/scivision/geo2mag/badge.svg?branch=master
    :target: https://coveralls.io/github/scivision/geo2mag?branch=master
.. image:: https://api.codeclimate.com/v1/badges/1f9596de34d1741ebc67/maintainability
   :target: https://codeclimate.com/github/scivision/geo2mag/maintainability
   :alt: Maintainability

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

    python -m pip install -e .

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
