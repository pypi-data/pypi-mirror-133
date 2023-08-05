# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isocrypt']

package_data = \
{'': ['*']}

install_requires = \
['humanfriendly>=10.0,<11.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['isocrypt = isocrypt.main:app']}

setup_kwargs = {
    'name': 'isocrypt',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Poe Rhiza',
    'author_email': 'poerhiz@gmail.com',
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
