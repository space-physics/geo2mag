#!/usr/bin/env python
"""
Loads site file, finds geomagnetic coordinates of sites
file can be xls(x), kml,kmz, h5
using http://wdc.kugi.kyoto-u.ac.jp/igrf/gggm/index.html
Michael Hirsch

ref:
http://pubs.usgs.gov/of/1999/ofr-99-0503/REPORT.HTM

"""
from datetime import datetime
from pandas import DataFrame
from matplotlib.pyplot import show
#
from geo2mag.io import loadsites
from geo2mag import loopcoord
from geo2mag.plots import plotgeomag
#
kmperdeglat = 111

def compdelta(latlon):
    assert isinstance(latlon,DataFrame)
    latlon.sort_values(by=['mlat','glat'],inplace=True)
    Dmlat_deg = latlon['mlat'].diff()
    Dglat_km = latlon['glat'].diff()*kmperdeglat

    return latlon,Dmlat_deg,Dglat_km


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='read site data and convert geographic/geodetic coordinates to geomagnetic coordinates')
    p.add_argument('fnyear',help='data file (or year)',nargs='?')
    p.add_argument('glat', help='latitude', nargs='?', type=float)
    p.add_argument('glon', help='longitude',nargs='?', type=float)
    p = p.parse_args()

    if p.glon is not None: # year, lat, lon
        year = int(p.fnyear)
        latlon = (p.glat, p.glon)
    else:
        latlon = loadsites(p.fnyear)
        year = datetime.now().year
#%% go to the cloud to compute magnetic coordinate from geodetic
    latlon = loopcoord(latlon, year)
#%% compute kilometers per magnetic degree lat vs. geodetic degree
    latlon,Dmlat_deg,Dglat_km = compdelta(latlon)
#%% plot
    plotgeomag(latlon)
    show()
