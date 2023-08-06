# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flaggart']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.2,<9.0.0', 'Wand>=0.6.7,<0.7.0', 'wikipedia>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'flaggart',
    'version': '0.4.1',
    'description': 'Package for retrieving, creating, and performing operations on flags',
    'long_description': None,
    'author': 'AlDacMac',
    'author_email': 'alasdairmacgdev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
