# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbpool']

package_data = \
{'': ['*']}

install_requires = \
['mysql-connector-python>=8.0.27,<9.0.0']

setup_kwargs = {
    'name': 'dbpool',
    'version': '1.2.0',
    'description': 'Enhance mysql-connector-python pooling',
    'long_description': None,
    'author': 'liyong',
    'author_email': 'hungrybirder@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hungrybirder/dbpool-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
