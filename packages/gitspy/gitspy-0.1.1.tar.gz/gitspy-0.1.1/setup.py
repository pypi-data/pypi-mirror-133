# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitspy']

package_data = \
{'': ['*']}

install_requires = \
['spall>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'gitspy',
    'version': '0.1.1',
    'description': 'Intuitive Git for Python',
    'long_description': 'gitspy\n======\n.. image:: https://github.com/jshwi/gitspy/actions/workflows/ci.yml/badge.svg\n    :target: https://github.com/jshwi/gitspy/actions/workflows/ci.yml\n    :alt: ci\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/pypi/v/gitspy\n    :target: https://img.shields.io/pypi/v/gitspy\n    :alt: pypi\n.. image:: https://codecov.io/gh/jshwi/gitspy/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/gitspy\n    :alt: codecov.io\n.. image:: https://img.shields.io/badge/License-MIT-blue.svg\n    :target: https://lbesson.mit-license.org/\n    :alt: mit\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\nIntuitive Git for Python\n\n\nInstall\n-------\nDependencies: git ^2.0.0 (tested)\n\n``pip install gitspy``\n\nDevelopment\n\n``poetry install``\n\nExample Usage\n-------------\n\nGet branch\n\n.. code-block:: python\n\n    >>> import gitspy\n    >>> git = gitspy.Git()\n    >>> # capture will store stdout, which can then be consumed by\n    >>> # calling `git.stdout()`\n    >>> # default is to print stdout, and stderr, to console\n    >>> returncode = git.symbolic_ref("--short", "HEAD", capture=True)\n    >>> print(returncode)  # printing returncode\n    0\n    >>> # consume stdout, a list containing a `str` of the checked out\n    >>> # branch\n    >>> stdout = git.stdout()  # -> [\'checked-out-branch\']\n    >>> items = len(stdout)  # printing length of `stdout()` outputs\n    >>> print(items)\n    1\n    >>> # no commands have been called yet since last call to `stdout`,\n    >>> # so stdout is empty\n    >>> stdout = git.stdout()  # -> []\n    >>> items = len(stdout)  # printing length of ``stdout()`` outputs\n    >>> print(items)\n    0\n    >>> # stdout can be accrued\n    >>> # [\'checked-out-branch\', \'checked-out-branch\']\n    >>> git.symbolic_ref("--short", "HEAD", capture=True)\n    >>> git.symbolic_ref("--short", "HEAD", capture=True)\n    >>> print(len(git.stdout()))\n    2\n    >>> # stdout is consumed\n    >>> print(len(git.stdout()))\n    0\n    >>> git.symbolic_ref("--short", "HEAD", capture=True)\n    >>> git.stdout()  # [...] -> void; clear stdout, if it exists\n    >>> print(len(git.stdout()))\n    0\n..\n\nGet commit hash\n\n.. code-block:: python\n\n    >>> import gitspy\n    >>> git = gitspy.Git()\n    >>> git.rev_parse("HEAD", capture=True)\n    >>> stored = git.stdout()[0]\n    >>> print(len(stored))  # print the length of the unique hash\n    40\n..\n',
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
