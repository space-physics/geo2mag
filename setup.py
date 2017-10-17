#!/usr/bin/env python
req = ['nose','numpy','lxml','beautifulsoup4','html5lib', 'requests', 'pandas', 'python-dateutil']
pipreq=['fastkml']

import pip
try:
    import conda.cli
    conda.cli.main('install',*req)
except Exception as e:
    pip.main(['install'] + req)
pip.main(['install'] + pipreq)

# %%
from setuptools import setup

setup(name='geo2mag',
      packages=['geo2mag'],
      install_requires=req+pipreq,
      author="Michael Hirsch, Ph.D.",
      url="https://github.com/scivision/geo2mag",
	  )
