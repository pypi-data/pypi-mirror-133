# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['canopy_viz']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.6,<6.0.0',
 'pyqtgraph>=0.12.3,<0.13.0',
 'pyserial>=3.5,<4.0',
 'python-can>=3.3.4,<4.0.0']

entry_points = \
{'console_scripts': ['canopy = canopy_viz.cli:main']}

setup_kwargs = {
    'name': 'canopy-viz',
    'version': '0.1.2',
    'description': 'visualize CAN bus payloads in realtime',
    'long_description': None,
    'author': 'TJ',
    'author_email': 'tbruno25@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
