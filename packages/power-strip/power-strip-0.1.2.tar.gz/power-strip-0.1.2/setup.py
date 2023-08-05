# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['power_strip', 'power_strip.v1alpha1']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-tools>=1.43.0,<2.0.0', 'grpcio>=1.43.0,<2.0.0']

setup_kwargs = {
    'name': 'power-strip',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'erdii',
    'author_email': 'me@erdii.engineering',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
