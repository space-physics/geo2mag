#!/usr/bin/env python
import pytest
from pytest import approx
import igrfcoord as ic


def test_geo2mag():
    latlon = ic.convert((65, -148, 2015), 'geomag')

    assert latlon['mlat'].item() == approx(65.56)
    assert latlon['mlon'].item() == approx(-96.46)


def test_mag2eo():
    latlon = ic.convert((65.56, -96.46, 2015), 'geodetic')

    assert latlon['glat'].item() == approx(65, abs=0.01)
    assert latlon['glon'].item() == approx(-148, abs=0.01)


if __name__ == '__main__':
    pytest.main(['-x', __file__])
