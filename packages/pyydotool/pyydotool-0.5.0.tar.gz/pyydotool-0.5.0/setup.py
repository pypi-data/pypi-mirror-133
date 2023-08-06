# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ydotool']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyydotool',
    'version': '0.5.0',
    'description': 'Python bindings to ydtool',
    'long_description': None,
    'author': 'Jerzy Drozdz',
    'author_email': 'jerzy.drozdz@jdsieci.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
