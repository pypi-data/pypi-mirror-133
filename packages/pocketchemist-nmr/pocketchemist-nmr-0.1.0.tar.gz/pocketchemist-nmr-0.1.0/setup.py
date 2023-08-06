# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pocketchemist_nmr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pocketchemist-nmr',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'J Lorieau',
    'author_email': 'justin@lorieau.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
