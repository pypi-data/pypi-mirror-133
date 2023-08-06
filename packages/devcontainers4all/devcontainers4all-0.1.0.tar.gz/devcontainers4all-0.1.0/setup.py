# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devcontainers4all']

package_data = \
{'': ['*']}

install_requires = \
['behave>=1.2.6,<2.0.0',
 'click-pathlib>=2020.3.13.0,<2021.0.0.0',
 'click>=8.0.3,<9.0.0',
 'commentjson>=0.9.0,<0.10.0',
 'docker>=5.0.3,<6.0.0',
 'logzero>=1.7.0,<2.0.0',
 'pexpect>=4.8.0,<5.0.0']

entry_points = \
{'console_scripts': ['dc = devcontainers4all.cli:run']}

setup_kwargs = {
    'name': 'devcontainers4all',
    'version': '0.1.0',
    'description': '',
    'long_description': '# devcontainers4all: Devcontainers without an IDE\n\n\n',
    'author': 'Cosimo Alfarano',
    'author_email': 'cosimo@alfarano.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
