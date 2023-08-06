# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gvol']

package_data = \
{'': ['*']}

install_requires = \
['gql[requests]==3.0.0rc0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['typing-extensions>=4.0.1,<5.0.0'],
 'docs': ['sphinx>=4.3.2,<5.0.0', 'sphinx-rtd-theme>=1.0.0,<2.0.0']}

setup_kwargs = {
    'name': 'gvol',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Denys Halenok',
    'author_email': 'denys.halenok@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
