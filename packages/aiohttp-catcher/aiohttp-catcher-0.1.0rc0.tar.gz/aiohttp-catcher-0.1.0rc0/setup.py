# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_catcher']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0']

setup_kwargs = {
    'name': 'aiohttp-catcher',
    'version': '0.1.0rc0',
    'description': 'A centralized error handler for aiohttp servers',
    'long_description': None,
    'author': 'Yuvi Herziger',
    'author_email': 'yherziger@immuta.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
