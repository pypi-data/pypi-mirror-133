# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fayouts',
 'fayouts.aiobot',
 'fayouts.calc',
 'fayouts.datetime',
 'fayouts.files',
 'fayouts.start']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fayouts',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Fakem1ner',
    'author_email': '87234992+Fakeminer@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
