# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zs_mixins']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3', 'Werkzeug>=2.0']

setup_kwargs = {
    'name': 'zs-mixins',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'codeif',
    'author_email': 'me@codeif.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
