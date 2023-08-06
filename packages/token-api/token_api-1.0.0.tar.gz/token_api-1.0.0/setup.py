# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['token_api']
setup_kwargs = {
    'name': 'token-api',
    'version': '1.0.0',
    'description': 'Make a Token encryption',
    'long_description': None,
    'author': 'OwoNicoo',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
