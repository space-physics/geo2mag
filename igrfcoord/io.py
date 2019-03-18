from pathlib import Path
from zipfile import ZipFile
import numpy as np
import pandas

from . import tag


def loadsites(fn: Path, year: int, out: str = 'geodetic') -> pandas.DataFrame:
    """
    txt/csv/xls/xlsx file should be arranged Nx3, lat, lon, alt each row

    Parameters
    ----------

    fn : pathlib.Path
        path to data file
    year : int
        year of coordinate
    out : str, optional
        want to convert to "geomag" or "geodetic" (default)

    coords : pandas.DataFrame
        converted data
    """
    fn = Path(fn).expanduser()

    if fn.suffix in ('.txt', '.csv'):
        latlon = np.genfromtxt(fn, delimiter=',', usecols=(0, 1))
    elif fn.suffix in ('.xls', '.xlsx'):
        latlon = pandas.read_excel(fn, parse_cols=[0, 1]).values
    elif fn.suffix in ('.kml', '.kmz'):
        latlon = _loadkml(fn)

    tagged = tag(latlon[:, 0], latlon[:, 1], year, out)

    return tagged


def _loadkml(fn: Path) -> np.ndarray:
    from fastkml import kml

    fn = Path(fn).expanduser()

    latlon = []
    names = []
    if fn.suffix == '.kmz':
        z = ZipFile(fn, 'r').open('doc.kml', 'r').read()
    else:  # .kml
        z = fn.read_bytes()

    k = kml.KML()
    k.from_string(z)

    for P in k.features():
        try:
            latlon.append(P.geometry.coords[0][:2][::-1])
            names.append(P.name)
        except AttributeError:
            pass

    return np.asarray(latlon)
