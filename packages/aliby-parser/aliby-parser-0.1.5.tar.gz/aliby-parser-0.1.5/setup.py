# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logfile_parser']

package_data = \
{'': ['*'], 'logfile_parser': ['grammars/*']}

setup_kwargs = {
    'name': 'aliby-parser',
    'version': '0.1.5',
    'description': 'Log files parser for aliby pipeline.',
    'long_description': None,
    'author': 'Julian Pietsch',
    'author_email': 'jpietsch@ed.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
