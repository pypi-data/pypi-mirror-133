# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coshed_ebusd']

package_data = \
{'': ['*']}

install_requires = \
['coshed-flask>=0.15.0,<0.16.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['cebusd-analysis = coshed_ebusd.cli:analysis_cli',
                     'cebusd-configuration-server = '
                     'coshed_ebusd.cli:configuration_server_cli']}

setup_kwargs = {
    'name': 'coshed-ebusd',
    'version': '0.2.0',
    'description': 'ebusd helper for lazy developer(s)',
    'long_description': None,
    'author': 'doubleO8',
    'author_email': 'wb008@hdm-stuttgart.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
