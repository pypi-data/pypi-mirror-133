# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['random_colors']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0']

setup_kwargs = {
    'name': 'random-colors',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Arnthor Jonsson',
    'author_email': 'arnthorj2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
