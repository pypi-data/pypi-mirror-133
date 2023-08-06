# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['agora', 'agora.io', 'agora.io.logfile_parser', 'agora.utils']

package_data = \
{'': ['*'], 'agora.io.logfile_parser': ['grammars/*']}

setup_kwargs = {
    'name': 'aliby-agora',
    'version': '0.2.0',
    'description': 'A gathering of shared utilities for the Swain Lab image processing pipeline.',
    'long_description': None,
    'author': 'Julian Pietsch',
    'author_email': 'jpietsch@ed.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
