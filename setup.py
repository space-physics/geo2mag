#!/usr/bin/env python
req = ['nose','numpy','lxml','beautifulsoup4','html5lib', 'requests', 'pandas', 'python-dateutil','fastkml']
# %%
from setuptools import setup,find_packages

setup(name='geo2mag',
      packages=find_packages(),
      install_requires=req,
      author="Michael Hirsch, Ph.D.",
      url="https://github.com/scivision/geo2mag",
      python_requires='>=3.6',
	  )
