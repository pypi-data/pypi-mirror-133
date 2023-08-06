# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['siwe', 'siwe.grammars']

package_data = \
{'': ['*']}

install_requires = \
['abnf==1.1.1',
 'eth-account>=0.5.6,<0.6.0',
 'python-dateutil==2.8.2',
 'web3>=5.26.0,<6.0.0']

setup_kwargs = {
    'name': 'siwe',
    'version': '0.0.1',
    'description': 'A Python implementation of Sign-In with Ethereum (EIP-4361).',
    'long_description': '# Sign-In with Ethereum\n\nA Python implementation of Sign-In with Ethereum.\n',
    'author': 'Spruce Systems, Inc.',
    'author_email': 'hello@spruceid.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://login.xyz',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
