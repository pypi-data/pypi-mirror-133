# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cliwrap']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cliwrap',
    'version': '0.2.1',
    'description': 'A lightweight wrapper around CLIs for error handling and logging.',
    'long_description': '# cliwrap-python\nA lightweight wrapper around CLIs for error handling and logging.\n',
    'author': 'Olivier Van Aken',
    'author_email': 'olivier.va@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
