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
    'version': '0.2.2',
    'description': 'Multirun is a simple wrapper around tmux to allow running and monitoring multiple processes at once',
    'long_description': 'Multirun\n========\n\nMultirun is a development tool to run and monitor services needed in the development process.\n\nQuickstart\n----------\n\nOnce installed `multirun` will be in your PATH. You will also need to build a toml file with the commands\nyou wish to run:\n\n```\n[redis]\ncmd = "make run_redis"\n\n[celery_worker]\ncmd = "make run_worker"\n\n[django]\ncmd = "make run_app"\n```\n\nthen run `multirun -c path/to/multirun.toml`  \n\nYou should see a screen similar to:\n\n![screenshot of multirun](screenshot.png)\n\nOnce running, you can click on individual panes to select them `C-b r` will kill and rerun the process, `C-b k` will kill all commands and exit multirun.',
    'author': 'Rob Sayers',
    'author_email': 'rsayers@robsayers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rsayers/multirun',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
