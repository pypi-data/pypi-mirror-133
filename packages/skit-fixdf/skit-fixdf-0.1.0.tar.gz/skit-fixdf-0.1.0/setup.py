# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skit_fixdf', 'skit_fixdf.fix']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.5,<2.0.0']

setup_kwargs = {
    'name': 'skit-fixdf',
    'version': '0.1.0',
    'description': "A library to format datasets so that you don't have to.",
    'long_description': None,
    'author': 'ltbringer',
    'author_email': 'amresh.venugopal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
