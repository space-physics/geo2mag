#!/usr/bin/env python
"""
from http://wdc.kugi.kyoto-u.ac.jp/igrf/gggm/
"""
import pytest
from geo2mag import geo2mag


@pytest.mark.parametrize(
    "glat,glon,mlat,mlon",
    [
        (79.3, 288.59, 88.880248, 11.379883),
        (
            [79.3, 79.3, 0, 90, -90, 45],
            [288.59, 288.583, 0, 90, -90, 150],
            [88.880248, 88.89, 2.88, 80.31, -80.31, 37.36],
            [11.379883, 11.68, 72.85, 180, 0, -142.82],
        ),
    ],
)
def test_geo2mag(glat, glon, mlat, mlon):
    ma, mo = geo2mag(glat, glon)

    assert ma == pytest.approx(mlat, rel=1e-3, abs=0.3)
    assert mo == pytest.approx(mlon, rel=1e-3, abs=0.4)

    if not isinstance(glat, float):
        assert len(mlat) == len(ma)


if __name__ == "__main__":
    pytest.main()
