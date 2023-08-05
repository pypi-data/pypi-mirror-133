# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aipkgs_core']

package_data = \
{'': ['*']}

install_requires = \
['email-validator>=1.1.3,<2.0.0',
 'emoji>=1.6.1,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'phonenumbers>=8.12.40,<9.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'aipkgs-core',
    'version': '0.0.3',
    'description': '',
    'long_description': "AI's package\n",
    'author': 'Alexy',
    'author_email': 'alexy.ib@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/aipy/common',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
