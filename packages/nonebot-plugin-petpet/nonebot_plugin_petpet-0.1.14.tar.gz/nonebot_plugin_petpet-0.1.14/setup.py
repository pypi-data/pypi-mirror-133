# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_petpet']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0',
 'httpx>=0.19.0',
 'imageio>=2.12.0,<3.0.0',
 'nonebot-adapter-cqhttp>=2.0.0-alpha.15,<3.0.0',
 'nonebot2>=2.0.0-alpha.15,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-petpet',
    'version': '0.1.14',
    'description': 'Nonebot2 plugin for making fun pictures',
    'long_description': None,
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
