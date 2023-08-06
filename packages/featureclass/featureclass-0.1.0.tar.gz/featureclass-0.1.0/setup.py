# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['featureclass']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'featureclass',
    'version': '0.1.0',
    'description': 'Feature engineering library that helps you keep track of feature dependencies, documentation and schema',
    'long_description': '# featureclass\nFeature engineering library that helps you keep track of feature dependencies, documentation and schema\n',
    'author': 'Itay Azolay',
    'author_email': 'itayazolay@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Itayazolay/featureclass',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
