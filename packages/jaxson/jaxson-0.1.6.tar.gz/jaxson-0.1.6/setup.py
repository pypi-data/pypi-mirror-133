# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jaxson']

package_data = \
{'': ['*']}

install_requires = \
['jax>=0.2.26,<0.3.0', 'jaxlib>=0.1.75,<0.2.0']

setup_kwargs = {
    'name': 'jaxson',
    'version': '0.1.6',
    'description': 'A generative art libary based on Jax',
    'long_description': None,
    'author': 'Sam Corzine',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
