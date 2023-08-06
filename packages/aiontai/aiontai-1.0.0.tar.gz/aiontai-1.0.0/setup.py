# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiontai']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'dataclasses-json>=0.5.6,<0.6.0',
 'injector>=0.19.0,<0.20.0',
 'schema>=0.7.5,<0.8.0']

setup_kwargs = {
    'name': 'aiontai',
    'version': '1.0.0',
    'description': 'Async wrapper for nhentai API',
    'long_description': None,
    'author': 'LEv145',
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
