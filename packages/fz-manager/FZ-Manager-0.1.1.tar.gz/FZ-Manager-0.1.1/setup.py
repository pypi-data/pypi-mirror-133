# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fz_manager']

package_data = \
{'': ['*']}

install_requires = \
['aioconsole>=0.3.3,<0.4.0',
 'prompt-toolkit>=3.0.24,<4.0.0',
 'questionary>=1.10.0,<2.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.26.0,<3.0.0',
 'rich>=10.16.1,<11.0.0',
 'websockets>=10.1,<11.0']

entry_points = \
{'console_scripts': ['fz-manager = fz_manager.main:main',
                     'fzm = fz_manager.main:main']}

setup_kwargs = {
    'name': 'fz-manager',
    'version': '0.1.1',
    'description': 'Factorio Zone Server Manager',
    'long_description': None,
    'author': 'michelsciortino',
    'author_email': 'michel.sciortino@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/michelsciortino/FZ-Manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
