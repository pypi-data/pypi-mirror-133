# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ccui', 'ccui.tools', 'ccui.utils']

package_data = \
{'': ['*']}

install_requires = \
['rich>=10.16.1,<11.0.0']

setup_kwargs = {
    'name': 'ccui',
    'version': '0.2.5',
    'description': "CatOw's Console User Interface - An interactive Console of tools",
    'long_description': None,
    'author': 'CatOw',
    'author_email': 'ccuiproject@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
