#!/usr/bin/env python
"""
Loads site file, finds geomagnetic coordinates of sites
file can be xls(x), kml,kmz, h5
using http://wdc.kugi.kyoto-u.ac.jp/igrf/gggm/index.html
Michael Hirsch

ref:
http://pubs.usgs.gov/of/1999/ofr-99-0503/REPORT.HTM

"""
import requests
from pandas import read_html,DataFrame,read_excel
from numpy import ndarray,genfromtxt,atleast_2d
from time import sleep
#
from geo2mag import Path
from geo2mag.io import loadkml
#
kmperdeglat = 111

def loadsites(fn):
    """
    txt/csv/xls/xlsx file should be arranged Nx3, lat, lon, alt each row
    """
    fn = Path(fn).expanduser()

    if fn.endswith('.txt') or fn.endswith('.csv'):
        return genfromtxt(fn, delimiter=',',usecols=(0,1))
    elif fn.endswith('.xls') or fn.endswith('.xlsx'):
        return read_excel(fn,parse_cols=[0,1]).values
    elif fn.endswith('.kml') or fn.endswith('.kmz'):
        return loadkml(fn)

def loopcoord(latlon):
    if isinstance(latlon,(ndarray,DataFrame)):
        if latlon.ndim==1:
            assert latlon.size in (2,3)
        elif latlon.ndim==2:
            assert latlon.shape[1] in (2,3)
        else:
            raise ValueError('1-D or 2-D array Nx2')

        if isinstance(latlon,ndarray):
            latlon = DataFrame(latlon,columns=['glat','glon'])

    elif isinstance(latlon,(tuple,list)):
        assert len(latlon) in (2,3)
        latlon = DataFrame(data=atleast_2d(latlon[:2]),columns=['glat','glon'])
    else:
        raise TypeError('I expect Nx2 array of lat,lon or len=2 vector in tuple or list')

    for n,l in latlon.iterrows():
        page = geo2mag(l['glat'],l['glon'])
        latlon.at[n,'mlat'],latlon.at[n,'mlon'] = geomag_table(page)
    return latlon

def geo2mag(glat,glon):
    sleep(1) #don't hammer the server
    #TODO for now just uses default year, at this time 2015
    root = 'http://wdc.kugi.kyoto-u.ac.jp/'

    pl = {'Lat':int(glat),'Latm':(glat-int(glat))*60,
          'Long':int(glon),'Longm':(glon-int(glon))*60}

    # NOTE: server default is N,E accepts -E for W

    with requests.session() as s:
        r=s.get(root+'igrf/gggm/index.html')
        if r.status_code==200:
            return s.post(root+'/cgi-bin/trans-cgi',data=pl).content

def geomag_table(page):
    tab = read_html(page,header=0,index_col=0)[0]
    tab.dropna(axis=0,how='all',inplace=True)

    s = tab.at['Geomagnetic','Latitude']
    if s[-1] == 'N':
        mlat = float(s[:-1])
    elif s[-1] == 'S':
        mlat = -float(s[:-1])
    else:
        raise ValueError('I expected N or S but got {}'.format(s[-1]))

    s = tab.at['Geomagnetic','Longitude']
    if s[-1] == 'W':
        mlon = -float(s[:-1])
    elif s[-1] == 'E':
        mlon = float(s[:-1])
    else:
        raise ValueError('I expected E or W but got {}'.format(s[-1]))

    return mlat,mlon #float must be above for - operator

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
