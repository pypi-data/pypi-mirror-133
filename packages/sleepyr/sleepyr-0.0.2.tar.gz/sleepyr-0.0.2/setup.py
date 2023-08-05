# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sleepyr']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'sleepyr',
    'version': '0.0.2',
    'description': 'Python Sleeper API client',
    'long_description': None,
    'author': 'Craig Martek',
    'author_email': 'craigmartek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/craigatron/sleepyr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
