# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zotero2readwise']

package_data = \
{'': ['*']}

install_requires = \
['Pyzotero>=1.4.26,<2.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'zotero2readwise',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ealizadeh',
    'author_email': 'alizadeh.essi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
