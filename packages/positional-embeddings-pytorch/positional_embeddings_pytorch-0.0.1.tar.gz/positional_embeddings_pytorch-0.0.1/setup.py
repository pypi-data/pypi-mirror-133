# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['positional_embeddings_pytorch']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.10.1,<2.0.0']

setup_kwargs = {
    'name': 'positional-embeddings-pytorch',
    'version': '0.0.1',
    'description': 'A collection of positional embeddings (or positional encodings) written in pytorch.',
    'long_description': None,
    'author': 'wusuowei60',
    'author_email': 'quym@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
