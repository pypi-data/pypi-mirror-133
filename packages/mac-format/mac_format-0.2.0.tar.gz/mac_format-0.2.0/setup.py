# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mac_format']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.0,<3.0.0']

setup_kwargs = {
    'name': 'mac-format',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Lucas',
    'author_email': 'lucasbmello96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
