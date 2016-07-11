#!/usr/bin/env python
from setuptools import setup
import subprocess

try:
    subprocess.call(['conda','install','--file','requirements.txt'])
except Exception as e:
    pass


setup(name='geo2mag',
	  description='Convert geodetic to geomagnetic coordinates',
      author='Michael Hirsch',
	  url='https://github.com/scienceopen/geo2mag',
      install_requires=['fastkml','pathlib2'],
      packages=['geo2mag'],
	  )
