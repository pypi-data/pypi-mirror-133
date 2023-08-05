# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot', 'nonebot.adapters.kaiheila', 'nonebot.adapters.kaiheila.v3']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'nonebot2>=2.0.0-beta.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-adapter-kaiheila',
    'version': '0.0.1',
    'description': 'kaiheila adapter for nonebot2',
    'long_description': '# nonebot-adapter-kaiheila\nnonebot adapter for kaiheila bot\n\n开黑啦 `nonebot` 适配器\n',
    'author': 'Tian-que',
    'author_email': '1605206150@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Tian-que/nonebot-adapter-kaiheila',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
