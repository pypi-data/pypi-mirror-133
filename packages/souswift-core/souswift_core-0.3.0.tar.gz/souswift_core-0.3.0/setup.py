# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['souswift_core', 'souswift_core.providers', 'souswift_core.providers.database']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.29,<2.0.0',
 'aiomysql>=0.0.22,<0.0.23',
 'context-handler>=2.1.0,<3.0.0',
 'starlette>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'souswift-core',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Gustavo Correa',
    'author_email': 'self.gustavocorrea@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
