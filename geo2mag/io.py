from __future__ import unicode_literals
from pathlib import Path
from zipfile import ZipFile
from pandas import DataFrame,read_excel
from numpy import asarray,genfromtxt


def loadsites(fn):
    """
    txt/csv/xls/xlsx file should be arranged Nx3, lat, lon, alt each row
    """
    fn = Path(fn).expanduser()

    ext = fn.suffix

    if ext in   ('.txt', '.csv'):
        return genfromtxt(fn, delimiter=',',usecols=(0,1))
    elif ext in ('.xls', '.xlsx'):
        return read_excel(fn, parse_cols=[0,1]).values
    elif ext in ('.kml', '.kmz'):
        return loadkml(fn)


def loadkml(fn):
    from fastkml import kml

    fn = Path(fn)

    latlon=[]
    names = []
    if fn.suffix=='.kmz':
        z = ZipFile(fn,'r').open('doc.kml','r').read()
    else: #.kml
        z = fn.open('r').read()

    k = kml.KML()
    k.from_string(z)

    for P in k.features():
        try:
            latlon.append(P.geometry.coords[0][:2][::-1])
            names.append(P.name)
        except AttributeError:
            pass

    return DataFrame(data=asarray(latlon).astype(float),
                     columns=['glat','glon'],
                     index=names)
