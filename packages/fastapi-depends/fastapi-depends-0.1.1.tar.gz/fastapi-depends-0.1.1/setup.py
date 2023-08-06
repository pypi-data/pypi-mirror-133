# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_depends']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.70.1,<0.71.0']

setup_kwargs = {
    'name': 'fastapi-depends',
    'version': '0.1.1',
    'description': 'Use your FastAPI dependencies in plain python code',
    'long_description': None,
    'author': 'troyan-dy',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/troyan-dy/fastapi-depends',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
