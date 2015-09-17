#!/usr/bin/env python3
"""
Loads .kmz file of sites, finds geomagnetic coordinates of sites
using http://wdc.kugi.kyoto-u.ac.jp/igrf/gggm/index.html
Michael Hirsch
"""
from zipfile import ZipFile
from pykml import parser
import requests
from pandas import read_html,DataFrame,read_excel,read_hdf
from numpy import asarray
from time import sleep
from os.path import splitext

kmperdeglat = 111

def loadsites(fn):
    if fn is None:
        return

    ext = splitext(fn)[1]

    if ext[:4] == '.xls':
        return read_excel(fn)
    elif ext == '.h5':
        return read_hdf(fn,'sites')
    elif ext[:3] == '.km':
        lla = loadkml(fn)
        for n,l in lla.iterrows():
            page = geo2mag(l['glat'],l['glon'])
            lla.at[n,'mlat'],lla.at[n,'mlon'] = geomag_table(page)
        return lla

def loadkml(fn):
    lonlatalt=[]
    names = []
    if fn[-1]=='z':
        z = ZipFile(fn,'r')
    else:
        z = fn

    root= parser.fromstring(z.open('doc.kml','r').read())

    for P in root.Document.Folder.Placemark:
        try:
            R =P.Point.coordinates.text.split(sep=',')
            lonlatalt.append(R)
            names.append(P.name.text)
        except AttributeError:
            pass

    return DataFrame(asarray(lonlatalt).astype(float)[:,[1,0]],
                     columns=['glat','glon'],
                     index=names)

def geo2mag(glat,glon):
    sleep(1) #don't hammer the server
    #TODO for now just uses default year, at this time 2015
    root = 'http://wdc.kugi.kyoto-u.ac.jp/'

    pl = {'Lat':int(glat),'Latm':(glat-int(glat))*60,
          'Long':int(glon),'Longm':(glon-int(glon))*60}

    with requests.session() as s:
        r=s.get(root+'igrf/gggm/index.html')
        if r.status_code==200:
            return s.post(root+'/cgi-bin/trans-cgi',data=pl).content

def geomag_table(page):
    tab = read_html(page,header=0,index_col=0)[0]
    tab.dropna(axis=0,how='all',inplace=True)

    s = tab.at['Geomagnetic','Latitude']
    if s[-1] == 'N':
        mlat = s[:-1]
    elif s[-1] == 'S':
        mlat = -s[:-1]

    s = tab.at['Geomagnetic','Longitude']
    if s[-1] == 'W':
        mlon = s[:-1]
    elif s[-1] == 'E':
        mlon = -s[:-1]

    return float(mlat),float(mlon)

def compdelta(lla):
    lla.sort(columns=['mlat','glat'],inplace=True)
    Dmlat_deg = lla['mlat'].diff()
    Dglat_km = lla['glat'].diff()*kmperdeglat
    return lla,Dmlat_deg,Dglat_km

def writesites(fn,lla):
    if fn is None:
        return

    ext = splitext(fn)[1]

    if ext[:4] == '.xls':
        lla.to_excel(fn)
    elif ext == '.h5':
        lla.to_hdf(fn,'sites')


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='read site data and convert geographic/geodetic coordinates to geomagnetic coordinates')
    p.add_argument('fn',help='data file')
    p.add_argument('-o','--ofn',help='output data file to write')
    p = p.parse_args()

    lla = loadsites(p.fn)

    lla,Dmlat_deg,Dglat_km = compdelta(lla)

    writesites(p.ofn,lla)

