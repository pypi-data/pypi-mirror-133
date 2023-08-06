# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ntfy_bark']
install_requires = \
['requests>=2.27.0,<3.0.0']

setup_kwargs = {
    'name': 'ntfy-bark',
    'version': '0.1.0',
    'description': 'Bark backend for ntfy',
    'long_description': None,
    'author': 'Cologler',
    'author_email': 'skyoflw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
