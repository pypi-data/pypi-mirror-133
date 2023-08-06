# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clickup_cz']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'clickup-cz',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Maicon Pantoja',
    'author_email': 'maiconobmep@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
