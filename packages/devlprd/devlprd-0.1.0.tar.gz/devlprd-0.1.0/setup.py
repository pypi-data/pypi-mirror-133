# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['devlprd']

package_data = \
{'': ['*']}

install_requires = \
['mypy>=0.910,<0.911',
 'pyserial>=3.5,<4.0',
 'pytest-asyncio>=0.15.1,<0.16.0',
 'pytest>=6.2.4,<7.0.0',
 'websockets>=9.1,<10.0']

setup_kwargs = {
    'name': 'devlprd',
    'version': '0.1.0',
    'description': 'Daemon for managing integrations with the FATNM DEVLPR',
    'long_description': None,
    'author': 'Ezra Boley',
    'author_email': 'eboley@wisc.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
