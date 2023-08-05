# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seamapi']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'seamapi',
    'version': '0.1.0',
    'description': "A Python Library for Seam's API https://getseam.com",
    'long_description': None,
    'author': 'Severin Ibarluzea',
    'author_email': 'seveibar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
