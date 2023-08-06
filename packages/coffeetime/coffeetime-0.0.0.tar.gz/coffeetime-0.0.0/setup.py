# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coffeetime']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'coffeetime',
    'version': '0.0.0',
    'description': 'Date/time API inspired by JavaScript Temporal',
    'long_description': None,
    'author': 'Jeroen Schot',
    'author_email': 'jeroenschot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
