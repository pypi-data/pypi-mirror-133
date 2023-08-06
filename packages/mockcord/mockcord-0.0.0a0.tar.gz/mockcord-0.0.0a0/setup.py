# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mockcord']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mockcord',
    'version': '0.0.0a0',
    'description': '',
    'long_description': None,
    'author': 'aru',
    'author_email': 'genericusername414@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
