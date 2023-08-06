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
    'version': '0.2.1',
    'description': '',
    'long_description': '\n# mac-format\n\nCLI tool to format any possible mac address input text to some pretermined mac formats.\n\nBy defaul, the tool will clean the MAC address delimiters and reformat the address in lower and upper case, using two chars by group notation (xx:xx:xx:xx:xx:xx).\n\nOnly the follow delimiters will be added to the final addresses:\n\n- Nothing.\n- Single space.\n- `:`\n- `-`\n- `_`\n- `.`\n\n---\n# Installation\n\nTo install the tool, run the follow [pip](https://pypi.org/project/pip/) command:\n\n```shell\n    $ python3 -m pip install mac-format\n```\n\nTo check if the tool is availabe, run:\n\n```shell\n    $ python3 -m pip freeze | grep mac-format\n```\n\nTo simply run the tool, you can execute it calling the python module follow by the mac address:\n\n```shell\n    $ python3 -m mac_format 77:62:76:5F:B0:85\n    \n    |  | M |: 7762765FB08\n    |  | m |: 7762765fb08\n    | : | M |: 77:62:76:5F:B0:85\n    | : | m |: 77:62:76:5f:b0:85\n    | - | M |: 77-62-76-5F-B0-85\n    | - | m |: 77-62-76-5f-b0-85\n    | _ | M |: 77_62_76_5F_B0_85\n    | _ | m |: 77_62_76_5f_b0_85\n    | . | M |: 77.62.76.5F.B0.85\n    | . | m |: 77.62.76.5f.b0.85\n    |   | M |: 77 62 76 5F B0 85\n    |   | m |: 77 62 76 5f b0 85\n    ------------------------------\n    The 7762765FB085\'s vendor is: Dell Inc.\n```\n\nIf you just run the tool withou the MAC (`$ python3 -m mac_format`) an input field will be opened:\n\n```shell\n    $ py -m mac_format\n    \n    Type the MAC address: 77.62.76-5f.b0.85 \n\n    |  | M |: 7762765FB08\n    |  | m |: 7762765fb08\n    | : | M |: 77:62:76:5F:B0:85\n    ...\n    The 7762765FB085\'s vendor is: Dell Inc.\n```\n\nTo became easy to run, you can create an alias, the follow command:\n\n```sudo echo \'alias macf="python3 -m mac_format"\' >> ~/.zshrc```\n\n* I\'m using zsh in my shell, please change to your favorite shell rc file.\n\nThen simply run `macf` in your shell to run the tool.\n',
    'author': 'Lucas',
    'author_email': 'lucasbmello96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lbmello/mac_format/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
