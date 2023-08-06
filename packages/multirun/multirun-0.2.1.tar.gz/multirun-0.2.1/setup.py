# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multirun']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['multirun = multirun:main']}

setup_kwargs = {
    'name': 'multirun',
    'version': '0.2.1',
    'description': 'Multirun is a simple wrapper around tmux to allow running and monitoring multiple processes at once',
    'long_description': None,
    'author': 'Rob Sayers',
    'author_email': 'rsayers@robsayers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
