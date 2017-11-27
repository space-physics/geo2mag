import requests
import pandas
import numpy as np
from time import sleep
import random
#
ROOT = 'http://wdc.kugi.kyoto-u.ac.jp/'

def loopcoord(latlon, year:int) -> pandas.DataFrame:
    if isinstance(latlon, pandas.DataFrame):
        if latlon.ndim==1:
            assert latlon.size in (2,3)
        elif latlon.ndim==2:
            assert latlon.shape[1] in (2,3)
        else:
            raise ValueError('1-D or 2-D array Nx2')
    elif isinstance(latlon,(tuple,list)):
        latlon = loopcoord(np.atleast_2d(latlon), year)
    elif isinstance(latlon, np.ndarray):
        assert latlon.ndim==2 and latlon.shape[1] in (2,3) # necessary to avoid "infinite recursion" error
        latlon = loopcoord(pandas.DataFrame(latlon,columns=['glat','glon']), year)
    else:
        raise TypeError('expect Nx2 array of lat,lon or len=2 vector in tuple or list')
# %%
    for n,l in latlon.iterrows():
        page = geo2mag(l['glat'], l['glon'], year)
        latlon.at[n,'mlat'], latlon.at[n,'mlon'] = geomag_table(page)

    return latlon


def geo2mag(glat, glon, year):
    sleep(random.randrange(1,3)) #don't hammer the server

    pl = {'Lat':int(glat), 'Latm':(glat-int(glat))*60,
          'Long':int(glon), 'Longm':(glon-int(glon))*60,
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
