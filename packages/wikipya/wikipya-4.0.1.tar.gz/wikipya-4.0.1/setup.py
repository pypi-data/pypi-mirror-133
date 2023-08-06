# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wikipya', 'wikipya.methods', 'wikipya.models']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'httpx>=0.21.2,<0.22.0',
 'pydantic>=1.9.0,<2.0.0',
 'tghtml>=1.0.6,<2.0.0']

setup_kwargs = {
    'name': 'wikipya',
    'version': '4.0.1',
    'description': 'A simple async python library for search pages and images in wikis',
    'long_description': None,
    'author': 'Daniel Zakharov',
    'author_email': 'daniel734@bk.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
