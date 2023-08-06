# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['apartheid']
install_requires = \
['Plexer>=1.1,<2.0']

setup_kwargs = {
    'name': 'apartheid',
    'version': '0.2.0',
    'description': 'A simple parser (e.g. to parse a C file)',
    'long_description': '',
    'author': 'Shawn Presser',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/shawwn/apartheid',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
