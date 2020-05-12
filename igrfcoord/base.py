import pandas
import numpy as np
import typing as T

from .web import get_geo2mag, get_mag2geo


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

    nans = np.empty_like(lat)
    nans = nans.fill(np.nan)

    if out == "m" or out.startswith("geomag"):
        coords = (lat, lon, nans, nans, year)
    elif out == "g" or out == "geodetic":
        coords = (nans, nans, lat, lon, year)

    latlon = pandas.DataFrame(np.column_stack(coords), columns=["glat", "glon", "mlat", "mlon", "year"])

    return latlon


def convert(latlon: T.Sequence[float], out: str) -> pandas.DataFrame:
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
        assert latlon.ndim == 2 and latlon.shape[1] == 5
    elif isinstance(latlon, (tuple, list)):
        latlon = tag(latlon[0], latlon[1], latlon[2], out)
    elif isinstance(latlon, np.ndarray):
        # each row: lat, lon, year
        assert latlon.ndim == 2 and latlon.shape[1] == 3  # necessary to avoid "infinite recursion" error
        latlon = tag(latlon[:, 0], latlon[:, 1], latlon[:, 2], out)
    else:
        raise TypeError("expect Nx2 array of lat,lon or len=2 vector in tuple or list")
    # %%
    for _, c in latlon.iterrows():
        if out == "m" or out.startswith("geomag"):
            page = get_geo2mag(c.at["glat"], c.at["glon"], c.at["year"])
            c.at["mlat"], c.at["mlon"] = _table(page, out)
        elif out == "g" or out == "geodetic":
            page = get_mag2geo(c.at["mlat"], c.at["mlon"], c.at["year"])
            c.loc["glat"], c.loc["glon"] = _table(page, out)
        else:
            raise ValueError('output must be "geomag" or "geodetic"')

    return latlon


def _table(page: str, out: str) -> T.Tuple[float, float]:
    tab = pandas.read_html(page, header=0, index_col=0)[0]
    tab.dropna(axis=0, how="all", inplace=True)

    if out == "g" or out == "geodetic":
        tag = "Geographic"
    elif out == "m" or out.startswith("geomag"):
        tag = "Geomagnetic"
    else:
        raise ValueError('coordinate type must be "geomag" or "geodetic"')

    s = tab.at[tag, "Latitude"]
    if s[-1] == "N":
        mlat = float(s[:-1])
    elif s[-1] == "S":
        mlat = -float(s[:-1])
    else:
        raise ValueError(f"I expected N or S but got {s[-1]}")

    s = tab.at[tag, "Longitude"]
    if s[-1] == "W":
        mlon = -float(s[:-1])
    elif s[-1] == "E":
        mlon = float(s[:-1])
    else:
        raise ValueError(f"I expected E or W but got {s[-1]}")

    return mlat, mlon  # float must be above for - operator
