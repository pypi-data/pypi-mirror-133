# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['custom_package', 'custom_package.models']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy-Utils==0.38.2',
 'SQLAlchemy==1.4.29',
 'alembic==1.7.5',
 'psycopg2-binary==2.9.3']

setup_kwargs = {
    'name': 'custom-package',
    'version': '0.1.0',
    'description': 'Demo Custom Package',
    'long_description': None,
    'author': 'MeetParikh01',
    'author_email': 'meet.parikh@tntra.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
