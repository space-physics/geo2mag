from . import Path
from zipfile import ZipFile
from pykml import parser
from pandas import DataFrame
from numpy import asarray

def loadkml(fn):
    fn = Path(fn)

    latlon=[]
    names = []
    if fn.endswith('z'):
        z = ZipFile(str(fn),'r').open('doc.kml','r').read()
    else:
        z = fn.open('r').read()

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