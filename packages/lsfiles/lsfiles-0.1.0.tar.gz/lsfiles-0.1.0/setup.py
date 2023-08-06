# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lsfiles']

package_data = \
{'': ['*']}

install_requires = \
['gitspy>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'lsfiles',
    'version': '0.1.0',
    'description': 'Path object VC index',
    'long_description': None,
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
