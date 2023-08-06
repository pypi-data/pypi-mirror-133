# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot', 'nonebot.adapters.cqhttp']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot']

setup_kwargs = {
    'name': 'nonebot-adapter-cqhttp',
    'version': '2.0.0b1',
    'description': 'OneBot(CQHTTP) adapter for nonebot2',
    'long_description': '<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/adapter-onebot/master/website/static/logo.png" width="500" alt="nonebot-adapter-onebot"></a>\n</p>\n\n<div align="center">\n\n# NoneBot-Adapter-OneBot\n\n_✨ OneBot 协议适配 ✨_\n\n</div>\n\n**Deprecated**, use `nonebot-adapter-onebot` instead.\n',
    'author': 'yanyongyu',
    'author_email': 'yyy@nonebot.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://v2.nonebot.dev/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
