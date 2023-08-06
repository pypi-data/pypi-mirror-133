# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lwc_common']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.0,<3.0.0']

setup_kwargs = {
    'name': 'lwc-common',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'AminuIsrael',
    'author_email': 'israel.aminu@data2bots.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
