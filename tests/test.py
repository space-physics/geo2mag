#!/usr/bin/env python
from numpy.testing import assert_allclose
from geo2mag.geo2mag_coord import loopcoord


latlon = loopcoord((65,-148))

assert_allclose(latlon.values[0,2:],[ 65.56, -96.46])