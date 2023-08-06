# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitspy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gitspy',
    'version': '0.1.0',
    'description': 'Intuitive Git for Python',
    'long_description': None,
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
