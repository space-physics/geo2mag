#!/usr/bin/env python3
"""
Loads site file, finds geomagnetic coordinates of sites
file can be xls(x), kml,kmz, h5
using http://wdc.kugi.kyoto-u.ac.jp/igrf/gggm/index.html
Michael Hirsch

ref:
http://pubs.usgs.gov/of/1999/ofr-99-0503/REPORT.HTM

"""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from pykml import parser
import requests
from pandas import read_html,DataFrame,read_excel
from numpy import asarray,ndarray,genfromtxt,atleast_2d
from time import sleep
from matplotlib.pyplot import figure,show

kmperdeglat = 111

def loadsites(fn):
    """
    txt/csv/xls/xlsx file should be arranged Nx3, lat, lon, alt each row
    """
    fn = str(Path(fn).expanduser())

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

def loadkml(fn:str):
    latlon=[]
    names = []
    if fn.endswith('z'):
        z = ZipFile(fn,'r').open('doc.kml','r').read()
    else:
        z = open(fn,'r').read()

    root= parser.fromstring(z)
    try:
        R=root.Document.Folder.Placemark
    except AttributeError:
        R=root.Placemark

    for P in R:
        try:
            C = P.Point.coordinates.text.split(sep=',')[:2][::-1]
            latlon.append(C)
            names.append(P.name.text)
        except AttributeError:
            pass

    return DataFrame(data=asarray(latlon).astype(float),
                     columns=['glat','glon'],
                     index=names)

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

def compdelta(latlon:DataFrame):
    latlon.sort_values(by=['mlat','glat'],inplace=True)
    Dmlat_deg = latlon['mlat'].diff()
    Dglat_km = latlon['glat'].diff()*kmperdeglat
    return latlon,Dmlat_deg,Dglat_km

def plotgeomag(lla):
    ax = figure().gca()
    for n,l in lla.iterrows():
        if isinstance(n,str):
            if n[:3] == 'HST':
                c='red'
            elif n == 'PFISR':
                c='blue'
            else:
                c='black'
        else:
            c=None

        ax.scatter(l['mlon'],l['mlat'],s=180,facecolors='none',edgecolors=c)

    ax.set_xlabel('magnetic longitude [deg.]')
    ax.set_ylabel('magnetic latitude [deg.]')
    ax.grid(True)
    ax.set_title('Sites vs. GeoMagnetic coordinates')
    for lon,lat,n in zip(lla['mlon'],lla['mlat'],lla.index):
        try:
            ax.text(lon,lat,n,ha='center',va='center',fontsize=8)
        except ValueError:
            pass

    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
#%%
    ax = figure().gca()
    for n,l in lla.iterrows():
        if isinstance(n,str):
            if n[:3] == 'HST':
                c='red'
            elif n == 'PFISR':
                c='blue'
            else:
                c='black'
        else:
            c=None

        ax.scatter(l['glon'],l['glat'],s=180,facecolors='none',edgecolors=c)

    ax.set_xlabel('geodetic longitude [deg.]')
    ax.set_ylabel('geodetic latitude [deg.]')
    ax.grid(True)
    ax.set_title('Sites vs. Geodetic coordinates')
    for lon,lat,n in zip(lla['glon'],lla['glat'],lla.index):
        try:
            ax.text(lon,lat,n,ha='center',va='center',fontsize=8)
        except ValueError:
            pass

    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)

if __name__ == '__main__':
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