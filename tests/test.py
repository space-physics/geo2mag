#!/usr/bin/env python
from numpy.testing import assert_allclose,run_module_suite
from geo2mag import loopcoord

def test_geo2magconv():
    latlon = loopcoord((65,-148), 2015)

    assert_allclose(latlon.values[0,2:],[ 65.56, -96.46])

if __name__ == '__main__':
    run_module_suite()
