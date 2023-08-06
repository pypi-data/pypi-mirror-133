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
    'version': '0.1.1',
    'description': 'Path object VC index',
    'long_description': 'lsfiles\n=======\n.. image:: https://github.com/jshwi/lsfiles/actions/workflows/ci.yml/badge.svg\n    :target: https://github.com/jshwi/lsfiles/actions/workflows/ci.yml\n    :alt: ci\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/pypi/v/lsfiles\n    :target: https://img.shields.io/pypi/v/lsfiles\n    :alt: pypi\n.. image:: https://codecov.io/gh/jshwi/lsfiles/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/lsfiles\n    :alt: codecov.io\n.. image:: https://img.shields.io/badge/License-MIT-blue.svg\n    :target: https://lbesson.mit-license.org/\n    :alt: mit\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\nPath object VC index\n\nInstall\n-------\n\n``pip install lsfiles``\n\nDevelopment\n-----------\n\n``poetry install``\n\nUsage\n-----\n\n\n.. code-block:: python\n\n    >>> from lsfiles import LSFiles\n    >>> from pathlib import Path\n    >>> files = LSFiles()  # begin with an empty index\n    >>> # the `LSFiles` object is a mutable sequence (list-like object)\n    >>> print(files)\n    <LSFiles []>\n    >>> # `lsfiles` is designed to work with `git`, and only versioned files\n    >>> # are indexed\n    >>> # $ git init\n    >>> files.populate()  # <LSFiles []>\n    >>> # $ git add .\n    >>> files.populate()  # <LSFiles [PosixPath(...), ...]>\n    >>> files.clear()  # clear the index\n    >>> print(files)\n    <LSFiles []>\n    >>> # as `lsfiles` is an index of unique file paths, its implementation\n    >>> # of extend prevents duplicates\n    >>> values = [Path.cwd() / "1", Path.cwd() / "1"]\n    >>> files.extend(values)  # <LSFiles [PosixPath(\'.../lsfiles/1\')]>\n    >>> files.clear()\n    >>> # reduce minimizes index to directories and individual files\n    >>> # the list value is returned, leaving `LSFiles` unaltered\n    >>> values = [\n    ...     Path.cwd() / "f1",\n    ...     Path.cwd() / \'d1\' / "1",\n    ...     Path.cwd() / \'d1\' / "2",\n    ... ]\n    >>> files.extend(values)\n    >>> files.reduce() # -> [PosixPath(\'.../f1\'), PosixPath(\'.../d1\')]\n    >>> # exclusions are evaluated by their basename, and does not have\n    >>> # have to be an absolute path\n    >>> # exclusions can be added on instantiation\n    >>> files = LSFiles("f1")\n    >>> # or with the add exclusions method\n    >>> files = LSFiles()\n    >>> files.add_exclusions()\n',
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
