# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ntfy_bark']
install_requires = \
['requests>=2.27.0,<3.0.0']

setup_kwargs = {
    'name': 'ntfy-bark',
    'version': '0.1.1',
    'description': 'Bark backend for ntfy',
    'long_description': '# ntfy-bark\n\n[Bark](https://github.com/Finb/bark) backend for ntfy.\n\n## Installation\n\n``` cmd\npip install ntfy-bark\n```\n\n## Usage\n\nAdd following lines to your `ntfy.yml`:\n\n``` yaml\nntfy_bark:\n    push_url: https://api.day.app/...\n```\n\nFinally, send message to your devices with `ntfy -b ntfy_bark send MSG`.\n',
    'author': 'Cologler',
    'author_email': 'skyoflw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cologler/ntfy-bark-python',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
