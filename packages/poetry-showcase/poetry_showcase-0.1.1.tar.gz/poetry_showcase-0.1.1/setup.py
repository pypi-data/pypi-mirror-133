# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_showcase']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poetry-showcase',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Ankit Saini',
    'author_email': 'nnkitsaini@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
