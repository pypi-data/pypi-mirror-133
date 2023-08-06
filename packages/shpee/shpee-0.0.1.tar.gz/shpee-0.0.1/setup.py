# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shpee']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.21.3,<0.22.0']

setup_kwargs = {
    'name': 'shpee',
    'version': '0.0.1',
    'description': 'Shopee Affiliate API Wrapper',
    'long_description': None,
    'author': 'Ngalim Siregar',
    'author_email': 'ngalim.siregar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
