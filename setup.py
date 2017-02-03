#!/usr/bin/env python
from setuptools import setup
try:
    import conda.cli
    conda.cli.main('install','--file','requirements.txt')
except Exception as e:
    print(e)


setup(name='geo2mag',
      install_requires=['fastkml'],
      packages=['geo2mag'],
	  )
