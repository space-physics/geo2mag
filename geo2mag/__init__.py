import requests
import pandas
import xarray
import numpy as np
from time import sleep
import random
from .io import loadsites
#
ROOT = 'http://wdc.kugi.kyoto-u.ac.jp/'

def loopcoord(latlon, year:int=None) -> xarray.DataArray:
    if isinstance(latlon, xarray.DataArray):
        assert latlon.ndim==2 and latlon.shape[1]==4
    elif isinstance(latlon, (tuple,list)):
        latlon = loadsites(None, year, latlon[0], latlon[1])
    elif isinstance(latlon, np.ndarray):
        assert latlon.ndim==2 and latlon.shape[1] in (2,3) # necessary to avoid "infinite recursion" error
        latlon = loadsites(None, year, latlon[:,0], latlon[:,1])
    else:
        raise TypeError('expect Nx2 array of lat,lon or len=2 vector in tuple or list')
# %%
    for l in latlon:
        page = geo2mag(l.loc['glat'].item(), l.loc['glon'].item(), l.year)
        l.loc['mlat'], l.loc['mlon'] = geomag_table(page)

    return latlon


def geo2mag(glat:float, glon:float, year:int):
    sleep(random.randrange(1,3)) #don't hammer the server

    pl = {'Lat':int(glat), 'Latm':(glat % 1)*60,
          'Long':int(glon), 'Longm':(glon % 1)*60,
          'Year':int(year)}

    # NOTE: server default is N,E accepts -E for W

    with requests.session() as s:
        r = s.get(ROOT+'igrf/gggm/index.html')
        if r.status_code==200:
            return s.post(ROOT+'/cgi-bin/trans-cgi',data=pl).content


def geomag_table(page):
    tab = pandas.read_html(page, header=0, index_col=0)[0]
    tab.dropna(axis=0,how='all',inplace=True)

    s = tab.at['Geomagnetic','Latitude']
    if s[-1] == 'N':
        mlat = float(s[:-1])
    elif s[-1] == 'S':
        mlat = -float(s[:-1])
    else:
        raise ValueError(f'I expected N or S but got {s[-1]}')

    s = tab.at['Geomagnetic','Longitude']
    if s[-1] == 'W':
        mlon = -float(s[:-1])
    elif s[-1] == 'E':
        mlon = float(s[:-1])
    else:
        raise ValueError(f'I expected E or W but got {s[-1]}')

    return mlat,mlon #float must be above for - operator
