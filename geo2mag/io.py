from __future__ import unicode_literals
from pathlib import Path
from zipfile import ZipFile
import numpy as np
import pandas
import xarray


def loadsites(fn:Path, year:int, glat:float=None, glon:float=None):
    """
    txt/csv/xls/xlsx file should be arranged Nx3, lat, lon, alt each row
    """
    if fn is not None:
        fn = Path(fn).expanduser()

        if fn.suffix in ('.txt', '.csv'):
            latlon = np.genfromtxt(fn, delimiter=',',usecols=(0,1))
        elif fn.suffix in ('.xls', '.xlsx'):
            latlon = pandas.read_excel(fn, parse_cols=[0,1]).values
        elif fn.suffix in ('.kml', '.kmz'):
            latlon = loadkml(fn)
    else:
        assert glat is not None and glon is not None, 'must specify year, glat, glon'
        latlon = (glat,glon)

# %%
    latlon = np.atleast_2d(latlon).astype(float) # NOTE: float necessary to create float DataArray
    latlon = xarray.DataArray(np.column_stack((latlon,np.empty_like(latlon))),
                              coords={'site':range(latlon.shape[0]),
                                      'latlon':['glat','glon','mlat','mlon']},
                              dims=['site','latlon'],
                              attrs={'year':year},)

    return latlon


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

    return np.asarray(latlon).astype(float)
