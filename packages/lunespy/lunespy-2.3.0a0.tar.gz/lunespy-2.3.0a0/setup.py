# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lunespy',
 'lunespy.client',
 'lunespy.client.transactions',
 'lunespy.client.transactions.alias',
 'lunespy.client.transactions.burn',
 'lunespy.client.transactions.cancel_lease',
 'lunespy.client.transactions.issue',
 'lunespy.client.transactions.lease',
 'lunespy.client.transactions.mass',
 'lunespy.client.transactions.reissue',
 'lunespy.client.transactions.transfer',
 'lunespy.client.wallet',
 'lunespy.server.address',
 'lunespy.server.blocks',
 'lunespy.server.nodes',
 'lunespy.server.transactions',
 'lunespy.utils',
 'lunespy.utils.crypto']

package_data = \
{'': ['*'],
 'lunespy': ['.git/*',
             '.git/hooks/*',
             '.git/info/*',
             '.git/logs/*',
             '.git/logs/refs/heads/*',
             '.git/objects/pack/*',
             '.git/refs/heads/*']}

install_requires = \
['base58>=2.1.0,<3.0.0',
 'pytest-parallel>=0.1.1,<0.2.0',
 'python-axolotl-curve25519>=0.4.1.post2,<0.5.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['log = lunespy.utils:changelog',
                     'semver = lunespy.utils:semantic_version']}

setup_kwargs = {
    'name': 'lunespy',
    'version': '2.3.0a0',
    'description': 'Library for communication with nodes in mainnet or testnet of the lunes-blockchain network Allows the automation of sending assets, issue end reissue tokens, leasing, registry, and create new wallet.',
    'long_description': "# LunesPy\n\n**The [old version](https://github.com/lunes-platform/lunespy/blob/main/deprecated) is being discontinued, but it can still be used at your own and risk.**\n\nLibrary for communication with nodes in mainnet or testnet of the lunes-blockchain network\nAllows the automation of **sending assets**, **issue end reissue tokens**, **lease** and **create new wallet**.\n\n\n## [What's new?](https://github.com/lunes-platform/lunespy/blob/main/CHANGELOG.md)\n\n\n## [How to use LunesPy?](https://blockchain.lunes.io/telescope/docs/sdk/getting_started)\n\n\n## [Want to contribute to LunesPy?](https://github.com/lunes-platform/lunespy/blob/main/CONTRIBUTING.md)\n\n\n## Contributors\n\nThanks to the following people who have contributed to this project:\n\n* [olivmath](https://github.com/olivmath)\n* [marcoslkz](https://github.com/marcoslkz)\n* [VanJustin](https://github.com/VanJustin)\n* [xonfps](https://github.com/xonfps)\n\n## Contact\n\nIf you want to contact me you can reach me at <development@lunes.io>.\n\n## License\n\n[Apache License Version 2.0](https://github.com/lunes-platform/lunespy/blob/main/LICENSE).\n",
    'author': 'Lunes Platform',
    'author_email': 'development@lunes.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
