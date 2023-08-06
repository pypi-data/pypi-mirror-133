# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unstar_pipfile']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'tomlkit>=0.8.0,<0.9.0']

entry_points = \
{'console_scripts': ['unstar-pipfile = unstar_pipfile.unstar_pipfile:unstar']}

setup_kwargs = {
    'name': 'unstar-pipfile',
    'version': '0.0.1a5',
    'description': 'If you have stars in your Pipfile, this tool is for you!',
    'long_description': '# unstar-pipfile\nIf you have stars in your Pipfile, this project is for you!\n\n[![test-workflow](https://github.com/purificant/unstar-pipfile/actions/workflows/test.yaml/badge.svg)](https://github.com/purificant/unstar-pipfile/actions/workflows/test.yaml)\n[![PyPI version](https://badge.fury.io/py/unstar-pipfile.svg)](https://badge.fury.io/py/unstar-pipfile)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n`unstar-pipfile` is a tool to scan `Pipfile.lock` and replace any stars in `Pipfile` with precise versions from the lock file.\n\n# Installation\n`pip install unstar-pipfile`',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/purificant/unstar-pipfile',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
