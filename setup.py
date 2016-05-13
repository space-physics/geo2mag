#!/usr/bin/env python3
from setuptools import setup
import subprocess

try:
    subprocess.run(['conda','install','--yes','--file','requirements.txt'])
except Exception as e:
    print('you will need to install packages in requirements.txt  {}'.format(e))

with open('README.rst','r') as f:
	long_description = f.read()

setup(name='geo2mag',
      version='0.1',
	  description='Convert geodetic to geomagnetic coordinates',
	  long_description=long_description,
	  author='Michael Hirsch',
	  url='https://github.com/scienceopen/geo2mag',
     install_requires=['pykml'],
      dependency_links = [],
    extras_require={},
      packages=['geo2mag'],
	  )
