# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfsiv_utils']

package_data = \
{'': ['*']}

install_requires = \
['DateTime>=4.3,<5.0',
 'black>=21.12b0,<22.0',
 'bs4>=0.0.1,<0.0.2',
 'dateparser>=1.1.0,<2.0.0',
 'loguru>=0.5.3,<0.6.0',
 'pathlib>=1.0.1,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2021.3,<2022.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.27.0,<3.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'cfsiv-utils',
    'version': '0.1.2',
    'description': 'A collection of Logging, Time, Date, Filehandling and webscraping functions',
    'long_description': None,
    'author': 'Conrad Storz',
    'author_email': 'conradstorz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
