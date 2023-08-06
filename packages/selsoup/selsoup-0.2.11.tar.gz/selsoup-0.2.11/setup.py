# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['selsoup']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0', 'selenium>=4.1.0,<5.0.0']

entry_points = \
{'console_scripts': ['selsoup = selsoup.selsoup:main']}

setup_kwargs = {
    'name': 'selsoup',
    'version': '0.2.11',
    'description': '',
    'long_description': None,
    'author': 'lemerchand',
    'author_email': 'phoenix.scooter@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
