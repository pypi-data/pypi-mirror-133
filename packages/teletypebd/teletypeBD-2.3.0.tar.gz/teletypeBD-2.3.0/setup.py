# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['teletypebd']
setup_kwargs = {
    'name': 'teletypebd',
    'version': '2.3.0',
    'description': '',
    'long_description': None,
    'author': 'aygumov_g',
    'author_email': 'gaadjik05@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
