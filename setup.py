#!/usr/bin/env python
install_requires = ['numpy','requests', 'pandas','lxml'] # lxml <-- pandas.read_html
tests_require = ['nose',]
# %%
from setuptools import setup,find_packages

setup(name='geo2mag',
      packages=find_packages(),
      python_requires='>=3.6',
      install_requires=install_requires,
      extras_require={'tests':tests_require,
                      'io':['fastkml'],
                      'plot':['matplotlib','cartopy']},
      tests_require=tests_require,
      author="Michael Hirsch, Ph.D.",
      url="https://github.com/scivision/geo2mag",
	  )
