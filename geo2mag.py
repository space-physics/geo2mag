#!/usr/bin/env python
"""
Loads site file, finds geomagnetic coordinates of sites
file can be xls(x), kml,kmz, h5
using http://wdc.kugi.kyoto-u.ac.jp/igrf/gggm/index.html
Michael Hirsch

ref:
http://pubs.usgs.gov/of/1999/ofr-99-0503/REPORT.HTM

"""
from pandas import DataFrame
#
from geo2mag.io import loadsites
from geo2mag.geo2mag_coord import loopcoord
#
kmperdeglat = 111

def compdelta(latlon):
    assert isinstance(latlon,DataFrame)
    latlon.sort_values(by=['mlat','glat'],inplace=True)
    Dmlat_deg = latlon['mlat'].diff()
    Dglat_km = latlon['glat'].diff()*kmperdeglat
    return latlon,Dmlat_deg,Dglat_km

if __name__ == '__main__':
    from matplotlib.pyplot import show
    from geo2mag.plots import plotgeomag
    #
    from argparse import ArgumentParser
    p = ArgumentParser(description='read site data and convert geographic/geodetic coordinates to geomagnetic coordinates')
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('fn',help='data file',nargs='?')
    g.add_argument('-c','--latlon',help='enter lat,lon instead of file',nargs=2,type=float)
    p = p.parse_args()

    if p.latlon:
        latlon = p.latlon
    else:
        latlon = loadsites(p.fn)
#%% go to the cloud to compute magnetic coordinate from geodetic
    latlon = loopcoord(latlon)
#%% compute kilometers per magnetic degree lat vs. geodetic degree
    latlon,Dmlat_deg,Dglat_km = compdelta(latlon)
#%% plot
    plotgeomag(latlon)
    show()
