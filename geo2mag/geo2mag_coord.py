import requests
from pandas import DataFrame,read_html
from numpy import ndarray,atleast_2d
from time import sleep

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
        raise ValueError(f'I expected N or S but got {s[-1]}')

    s = tab.at['Geomagnetic','Longitude']
    if s[-1] == 'W':
        mlon = -float(s[:-1])
    elif s[-1] == 'E':
        mlon = float(s[:-1])
    else:
        raise ValueError(f'I expected E or W but got {s[-1]}')

    return mlat,mlon #float must be above for - operator
