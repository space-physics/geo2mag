=======
geo2mag
=======

Convert geodetic coordinates to geomagnetic coordinates, using the `hosted algorithm <http://wdc.kugi.kyoto-u.ac.jp/igrf/gggm/index.html>`_


Installation
============
::

  pip install pykml
  conda install --file requirements.txt
  
Usage
=====
Convert .KMZ file containing geodetic coordinates to geomagnetic coordinates, and save in an .XLSX file::

  ./geo2mag.py myfile.kmz -o myfile.xlsx
  
Convert .KMZ file containing geodetic coordinates to geomagnetic coordinates, and save in an .HDF5 file::

  ./geo2mag.py myfile.kmz -o myfile.h5
