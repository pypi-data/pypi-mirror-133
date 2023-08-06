# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pd_cli']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.20.5,<2.0.0', 'docker>=5.0.3,<6.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['pd = pd_cli.main:app', 'python-deploy = pd_cli.main:app']}

setup_kwargs = {
    'name': 'pd-cli',
    'version': '1.1.0',
    'description': 'CLI for https://pythondeploy.co/.',
    'long_description': '=================\nPython Deploy CLI\n=================\n\n.. image:: https://badge.fury.io/py/pd-cli.svg\n    :target: https://badge.fury.io/py/pd-cli\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n\nUsage\n-----\n\n1. Install `pd_cli` with `pipx`_.\n\n   .. code-block:: console\n\n    pipx install pd_cli\n\n2. Run `python-deploy --help` (or `pd --help`)\n\n`Python Deploy`_\n\n.. _Python Deploy: https://pythondeploy.co\n.. _pipx: https://pythondeploy.co\n',
    'author': 'Federico Jaramillo Martínez',
    'author_email': 'federicojaramillom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pythondeploy/cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
