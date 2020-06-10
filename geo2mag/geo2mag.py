import numpy as np
import typing as T
import argparse


def geo2mag(glat: float, glon: float) -> T.Tuple[float, float]:
    """
    Converts GEOGRAPHIC (latitude,longitude) to GEOMAGNETIC (latitude, longitude).
    Ground-level altitude
    This is just a rotation, so the accuracy is low compared to actual
    geomagnetic models like WMM, IGRF, etc.

    Latitudes and longitudes (east, 0..360) are expressed in degrees.
    They may be SCALAR, LIST or Numpy.ndarray (any shape and rank)

    > geo2mag(79.3,288.59) == pytest.approx([89.999992, -173.02325])


    Written by Pascal Saint-Hilaire (Saint-Hilaire@astro.phys.ethz.ch), May 2002
    https://github.com/wlandsman/IDLAstro

    converted to Python by Michael Hirsch June 2020

    http://wdc.kugi.kyoto-u.ac.jp/poles/polesexp.html "geomagnetic south pole"
    """

    # longitude (in degrees east) of Earth's magnetic south pole
    # 2015
    Dlong = 360 - (180 - 107.4)
    Dlat = 80.4

    # 1995
    # Dlong=288.59
    # Dlat=79.30

    Dlong = np.radians(Dlong)
    Dlat = np.radians(Dlat)

    R = 1

    glat = np.radians(glat)
    glon = np.radians(glon)
    galt = R

    # %% handle array shape
    glat_shape = glat.shape
    glon_shape = glon.shape

    glat = glat.ravel()
    glon = glon.ravel()

    # %% convert to rectangular coordinates
    #       X-axis: defined by the vector going from Earth's center towards
    #            the intersection of the equator and Greenwitch's meridian.
    #       Z-axis: axis of the geographic poles
    #       Y-axis: defined by Y=Z^X
    x = galt * np.cos(glat) * np.cos(glon)
    y = galt * np.cos(glat) * np.sin(glon)
    z = galt * np.sin(glat)

    # %% Compute 1st rotation matrix
    # rotation around plane of the equator,
    # from the Greenwich meridian to the meridian containing the magnetic
    # dipole pole.
    geolong2maglong = np.zeros((3, 3))
    geolong2maglong[0, 0] = np.cos(Dlong)
    geolong2maglong[1, 0] = np.sin(Dlong)
    geolong2maglong[0, 1] = -np.sin(Dlong)
    geolong2maglong[1, 1] = np.cos(Dlong)
    geolong2maglong[2, 2] = 1.0
    out = geolong2maglong.T @ np.array([x, y, z])

    # %% Second rotation
    # in the plane of the current meridian from geographic
    #                  pole to magnetic dipole pole.
    tomaglat = np.zeros((3, 3))
    tomaglat[0, 0] = np.cos(np.pi / 2 - Dlat)
    tomaglat[2, 0] = -np.sin(np.pi / 2 - Dlat)
    tomaglat[0, 2] = np.sin(np.pi / 2 - Dlat)
    tomaglat[2, 2] = np.cos(np.pi / 2 - Dlat)
    tomaglat[1, 1] = 1.0
    out = tomaglat.T @ out

    # %% convert back to latitude, longitude and altitude
    mlat = np.arctan2(out[2], np.sqrt(out[0] ** 2 + out[1] ** 2))
    mlat = np.degrees(mlat)
    mlon = np.arctan2(out[1], out[0])
    mlon = np.degrees(mlon)
    # malt=sqrt(out[0,*]^2+out[1,*]^2+out[2,*]^2)-R

    return mlat.reshape(glat_shape), mlon.reshape(glon_shape)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "latlon", help="geographic latitude, longitude (east, 0..360)", nargs=2, type=float,
    )
    p = p.parse_args()

    mlat, mlon = geo2mag(*p.latlon)

    print("mlat:", mlat, "mlon", mlon)
