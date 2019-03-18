import requests
import pandas
import numpy as np
from time import sleep
import random
from typing import Sequence, Tuple

ROOT = 'http://wdc.kugi.kyoto-u.ac.jp/'  # not yet https...
TIMEOUT = 15  # seconds, arbitrary


def tag(lat: float, lon: float, year: int, out: str) -> pandas.DataFrame:
    """
    puts data into a pandas.DataFrame for convenience

    Parameters
    ----------

    lat : float
        latitude
    lon : float
        longitude
    year : int
        year
    out : str
        geomag or geodetic

    Returns
    -------

    coords : pandas.DataFrame
        labeled data
    """

    # NOTE: float necessary to create float DataFrame
    lat = np.atleast_1d(lat).astype(float)
    lon = np.atleast_1d(lon).astype(float)
    year = np.atleast_1d(year)

    if out == 'm' or out.startswith('geomag'):
        coords = (lat, lon, np.empty_like(lat), np.empty_like(lat), year)
    elif out == 'g' or out == 'geodetic':
        coords = (np.empty_like(lat), np.empty_like(lat), lat, lon, year)

    latlon = pandas.DataFrame(np.column_stack(coords),
                              columns=['glat', 'glon', 'mlat', 'mlon', 'year'])

    return latlon


def convert(latlon: Sequence[float], out: str) -> pandas.DataFrame:
    """
    convert geomag <-> geodetic coordinates using web IGRF service

    Parameters
    ----------

    latlon : tuple of lat, lon, year
        latitude, longitude, year
    out : str
        "geomag" or "geodetic"

    Returns
    -------
    coords : pandas.DataFrame
        converted data
    """
    if isinstance(latlon, pandas.DataFrame):
        assert latlon.ndim == 2 and latlon.shape[1] == 4
    elif isinstance(latlon, (tuple, list)):
        latlon = tag(*latlon, out)
    elif isinstance(latlon, np.ndarray):
        # each row: lat, lon, year
        assert latlon.ndim == 2 and latlon.shape[1] == 3  # necessary to avoid "infinite recursion" error
        latlon = tag(latlon[:, 0], latlon[:, 1], latlon[:, 2], out)
    else:
        raise TypeError('expect Nx2 array of lat,lon or len=2 vector in tuple or list')
# %%
    for _, c in latlon.iterrows():
        if out == 'm' or out.startswith('geomag'):
            page = _geo2mag_get(c.at['glat'], c.at['glon'], c.at['year'])
            c.at['mlat'], c.at['mlon'] = _table(page, out)
        elif out == 'g' or out == 'geodetic':
            page = _mag2geo_get(c.at['mlat'], c.at['mlon'], c.at['year'])
            c.loc['glat'], c.loc['glon'] = _table(page, out)
        else:
            raise ValueError('output must be "geomag" or "geodetic"')

    return latlon


def _geo2mag_get(lat: float, lon: float, year: int) -> str:

    sleep(random.randrange(1, 3))  # don't hammer the server

    pl = {'Lat': int(lat), 'Latm': (lat % 1)*60,
          'Long': int(lon), 'Longm': (lon % 1)*60,
          'Year': int(year),
          'GGM': 0}

    # NOTE: server default is N,E accepts -E for W

    with requests.session() as s:
        r = s.get(ROOT+'igrf/gggm/index.html', timeout=TIMEOUT)
        if r.status_code != 200:
            raise ConnectionError('could not connect to IGRF server, status {}'.format(r.status_code))

        return s.post(ROOT+'/cgi-bin/trans-cgi', data=pl).text  # type: ignore


def _mag2geo_get(lat: float, lon: float, year: int) -> str:
    sleep(random.randrange(1, 3))  # don't hammer the server

    pl = {'Lat': int(lat), 'Latm': (lat - int(lat))*60,
          'Long': int(lon), 'Longm': (lon - int(lon))*60,
          'Year': int(year),
          'GGM': 1}

    # NOTE: server default is N,E accepts -E for W

    with requests.session() as s:
        r = s.get(ROOT+'igrf/gggm/index.html', timeout=TIMEOUT)
        if r.status_code != 200:
            raise ConnectionError('could not connect to IGRF server, status {}'.format(r.status_code))

        return s.post(ROOT+'/cgi-bin/trans-cgi', data=pl).text  # type: ignore


def _table(page: str, out: str) -> Tuple[float, float]:
    tab = pandas.read_html(page, header=0, index_col=0)[0]
    tab.dropna(axis=0, how='all', inplace=True)

    if out == 'g' or out == 'geodetic':
        tag = 'Geographic'
    elif out == 'm' or out.startswith('geomag'):
        tag = 'Geomagnetic'
    else:
        raise ValueError('coordinate type must be "geomag" or "geodetic"')

    s = tab.at[tag, 'Latitude']
    if s[-1] == 'N':
        mlat = float(s[:-1])
    elif s[-1] == 'S':
        mlat = -float(s[:-1])
    else:
        raise ValueError(f'I expected N or S but got {s[-1]}')

    s = tab.at[tag, 'Longitude']
    if s[-1] == 'W':
        mlon = -float(s[:-1])
    elif s[-1] == 'E':
        mlon = float(s[:-1])
    else:
        raise ValueError(f'I expected E or W but got {s[-1]}')

    return mlat, mlon  # float must be above for - operator
