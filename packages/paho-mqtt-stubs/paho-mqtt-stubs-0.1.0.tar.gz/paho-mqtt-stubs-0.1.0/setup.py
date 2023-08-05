# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paho-stubs']

package_data = \
{'': ['*'], 'paho-stubs': ['mqtt/*']}

install_requires = \
['paho-mqtt>=1.6.1,<2.0.0', 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'paho-mqtt-stubs',
    'version': '0.1.0',
    'description': 'Type stubs for the paho MQTT client library',
    'long_description': None,
    'author': 'Dániel Hagyárossy',
    'author_email': 'd.hagyarossy@sapstar.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/atraides/paho-mqtt-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
