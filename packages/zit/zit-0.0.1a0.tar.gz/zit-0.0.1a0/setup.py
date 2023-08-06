# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zit',
    'version': '0.0.1a0',
    'description': 'CLI for Zityspace API',
    'long_description': None,
    'author': 'Zityspace',
    'author_email': 'team@zityspace.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
