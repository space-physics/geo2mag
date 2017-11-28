#!/usr/bin/env python
"""
Loads site file, finds geomagnetic coordinates of sites
file can be xls(x), kml,kmz, h5

http://wdc.kugi.kyoto-u.ac.jp/igrf/gggm/index.html

Michael Hirsch

ref:
http://pubs.usgs.gov/of/1999/ofr-99-0503/REPORT.HTM

"""
from matplotlib.pyplot import show
#
from geo2mag.io import loadsites
from geo2mag import loopcoord
from geo2mag.plots import plotgeomag


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='read site data and convert geographic/geodetic coordinates to geomagnetic coordinates')
    p.add_argument('-f','--fn',help='data file')
    p.add_argument('year', help='year',type=int)
    p.add_argument('glat', help='geographic latitude', nargs='?', type=float)
    p.add_argument('glon', help='geographic longitude',nargs='?', type=float)
    p = p.parse_args()

    latlon = loadsites(p.fn, p.year, p.glat, p.glon)
#%% go to the cloud to compute magnetic coordinate from geodetic
    latlon = loopcoord(latlon)
#%% plot
    plotgeomag(latlon)
    show()
