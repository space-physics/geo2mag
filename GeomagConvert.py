#!/usr/bin/env python
"""
Loads site file, finds geomagnetic coordinates of sites

outputs pandas.DataFrame

http://wdc.kugi.kyoto-u.ac.jp/igrf/gggm/index.html

Michael Hirsch, Ph.D.

ref:
http://pubs.usgs.gov/of/1999/ofr-99-0503/REPORT.HTM

example:
    python GeomagConvert.py 2015 -c 65 -148 geomag

> 65.56 -96.46

    python GeomagConvert.py 2015 -c 65.56 -96.46 geodetic

> 65.004 -147.994

"""
from argparse import ArgumentParser

from igrfcoord import convert


def main():
    p = ArgumentParser(description=' convert coordinates: geographic/geodetic <=> geomagnetic')
    p.add_argument('year', help='year', type=int)
    g = p.add_mutually_exclusive_group()
    g.add_argument('-c', '--latlon', help='latitude, longitude', type=float, nargs=2)
    g.add_argument('-f', '--fn', help='data file')
    p.add_argument('out', help='do you want "geomag" or "geodetic" output?')
    P = p.parse_args()

    if P.fn:
        from matplotlib.pyplot import show
        from igrfcoord.io import loadsites
        from igrfcoord.plots import plotgeomag

        latlon = loadsites(P.fn, P.year, P.out)
        latlon = convert(latlon, P.out)

        plotgeomag(latlon)
        show()
    else:
        C = convert((*P.latlon, P.year), P.out)
        if P.out == 'geomag':
            print(C['mlat'].item(), C['mlon'].item())
        else:
            print(C['glat'].item(), C['glon'].item())


if __name__ == '__main__':
    main()
