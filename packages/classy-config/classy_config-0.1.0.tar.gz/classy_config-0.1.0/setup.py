# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classy_config']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'classy-config',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'GDWR',
    'author_email': 'gregory.dwr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
