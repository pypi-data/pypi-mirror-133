# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alignunformeval']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.5,<2.0.0', 'scipy>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'alignunformeval',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'akiFQC',
    'author_email': 'yakaredori@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
