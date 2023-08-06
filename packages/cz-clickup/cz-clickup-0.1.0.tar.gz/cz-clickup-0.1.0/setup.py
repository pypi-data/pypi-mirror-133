# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cz_clickup']
setup_kwargs = {
    'name': 'cz-clickup',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Maicon Pantoja',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
