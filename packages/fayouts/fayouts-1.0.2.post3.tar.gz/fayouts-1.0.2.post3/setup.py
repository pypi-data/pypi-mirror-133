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
    'version': '1.0.2.post3',
    'description': 'fayouts by fakeminer',
    'long_description': "# Datetime Module\nDatetime allows you to work with the current date and time. It adds only one function, and it allows you to get the date and time. Datetime is based on your PC's time zone.\n## Datetime Docs\nFirst, you need to call the getData () function, which is called without parameters, then in square brackets you should indicate what you want to get, for example minutes.\n```python\n1| print(getData()['minutes'])\n31\n1| print(getData()['year'])\n2022\n1| print(getData()['dateUs'])\n03.01.2022\n1| print(getData)['weekday']\nMonday\n```\n\n# Start Module\nThe Start Module allows you to create a new Python project, it creates a whole tree, including files, folders for source files, and so on. The module is called by a single import in a python file.\n## Start Docs\n1 Create a folder with the name of your project\n\n2 Create a main.py file in the root of the folder\n\n3 In the file, write the following command\n```python \n1| import fayouts.start.newproject\n```\n4 Run the main.py file, after creating the project, delete it\n\n# Files Module\nThe Files module lets you work with files much easier than in the original Python.\n# Files Docs\nFunctions\n\n1 writeFile will let you write anything to a file\n\n2 readFile will allow you to read all text from a file\n\n3 addToFile will allow you to add some text to the file\nDifferences:\nPython\n```python\nfile = open('name.txt', 'w')\nfile.write('Some text')\nfile.close()\n```\nFayouts\n```python\nwriteFile('name.txt', 'Some text')\n```\nPython\n```python\nfile = open('name.txt', 'r')\nprint(file.read())\nfile.close()\n```\nFayouts\n```python\nprint(readFile('name.txt'))\n```\n# Aiobot Module\nSo far, the Aiobot module only allows you to create a template for the aiogram project, but soon there will be much more options. Unfortunately, it is impossible to guess exactly the structure of each bot, so my module creates just a simple template that everyone needs. I do not want to shove everything that is possible into this module at once, this is wrong, because this is how all customization disappears, all the opportunity to customize the bot for yourself.\n## Aiobot Docs\nTo create a project, you need to create a main.py file and write:\n```python\nimport fayouts.aiobot.startproject\n```\nYou can configure the bot in config.py, you must store all your filters in filters.py, and everything related to the bot itself in bot.py.\nbot.py is the entry point to your bot's program",
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
