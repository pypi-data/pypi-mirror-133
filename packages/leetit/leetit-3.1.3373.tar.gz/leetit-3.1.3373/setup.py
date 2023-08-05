# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leetit', 'leetit.leetit', 'leetit.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'leetit',
    'version': '3.1.3373',
    'description': '1337 translator lib',
    'long_description': '# leetit\n1337 translator lib\n',
    'author': 'DomesticMoth',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DomesticMoth/leetit',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
