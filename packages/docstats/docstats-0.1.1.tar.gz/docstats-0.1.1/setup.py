# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docstats', 'docstats.directives']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=4.3.2,<5.0.0']

setup_kwargs = {
    'name': 'docstats',
    'version': '0.1.1',
    'description': 'Statistics and other numbers for your sphinx pages',
    'long_description': None,
    'author': 'GameDungeon',
    'author_email': 'gamedungeon@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
