# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wm_ssh']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['wm-ssh = wm_ssh.cli:wm_ssh']}

setup_kwargs = {
    'name': 'wm-ssh',
    'version': '0.1.0',
    'description': 'Wikimedia ssh wrapper to expand host names',
    'long_description': None,
    'author': 'David Caro',
    'author_email': 'me@dcaro.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
