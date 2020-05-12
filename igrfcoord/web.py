from time import sleep
import random
import requests

ROOT = "http://wdc.kugi.kyoto-u.ac.jp/"  # not yet https...
TIMEOUT = 15  # seconds, arbitrary


def get_geo2mag(lat: float, lon: float, year: int) -> str:

    sleep(random.randrange(1, 3))  # don't hammer the server

    pl = {"Lat": int(lat), "Latm": (lat % 1) * 60, "Long": int(lon), "Longm": (lon % 1) * 60, "Year": int(year), "GGM": 0}

    # NOTE: server default is N,E accepts -E for W

    with requests.session() as s:
        r = s.get(ROOT + "igrf/gggm/index.html", timeout=TIMEOUT)
        if r.status_code != 200:
            raise ConnectionError("could not connect to IGRF server, status {}".format(r.status_code))

        return s.post(ROOT + "/cgi-bin/trans-cgi", data=pl).text  # type: ignore


def get_mag2geo(lat: float, lon: float, year: int) -> str:
    sleep(random.randrange(1, 3))  # don't hammer the server

    pl = {
        "Lat": int(lat),
        "Latm": (lat - int(lat)) * 60,
        "Long": int(lon),
        "Longm": (lon - int(lon)) * 60,
        "Year": int(year),
        "GGM": 1,
    }

    # NOTE: server default is N,E accepts -E for W

    with requests.session() as s:
        r = s.get(ROOT + "igrf/gggm/index.html", timeout=TIMEOUT)
        if r.status_code != 200:
            raise ConnectionError("could not connect to IGRF server, status {}".format(r.status_code))

        return s.post(ROOT + "/cgi-bin/trans-cgi", data=pl).text  # type: ignore
