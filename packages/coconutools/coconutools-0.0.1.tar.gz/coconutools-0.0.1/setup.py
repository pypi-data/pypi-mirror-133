# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coconutools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'coconutools',
    'version': '0.0.1',
    'description': 'Modern API for good old MS-COCO CV dataset format',
    'long_description': None,
    'author': 'Roman Glushko',
    'author_email': 'roman.glushko.m@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
