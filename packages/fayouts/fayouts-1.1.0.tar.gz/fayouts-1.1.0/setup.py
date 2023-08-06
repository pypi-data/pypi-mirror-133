# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fayouts',
 'fayouts.aiobot',
 'fayouts.calc',
 'fayouts.datetime',
 'fayouts.discobot',
 'fayouts.fayouts',
 'fayouts.files',
 'fayouts.start']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fayouts',
    'version': '1.1.0',
    'description': 'Fayouts can do a lot, but they are just a tool',
    'long_description': "# Datetime Module\nDatetime allows you to work with the current date and time. It adds only one function, and it allows you to get the date and time. Datetime is based on your PC's time zone.\n## Datetime Docs\nFirst, you need to call the getData () function, which is called without parameters, then, separated by a period, you should indicate what you want to get, for example, minutes.\n```python\n1| print(getData().minutes)\n31\n1| print(getData().year)\n2022\n1| print(getData().dateUs)\n03.01.2022\n1| print(getData().weekday)\nMonday\n```\n\n# Start Module\nThe Start Module allows you to create a new Python project, it creates a whole tree, including files, folders for source files, and so on. The module is called by a single import in a python file.\n## Start Docs\n1 Create a folder with the name of your project\n\n2 Create a main.py file in the root of the folder\n\n3 In the file, write the following command\n```python \n1| import fayouts.start.newproject\n```\n4 Run the main.py file, after creating the project, delete it\n\n# Files Module\nThe Files module lets you work with files much easier than in the original Python.\n## Files Docs\nFunctions\n\n1 writeFile will let you write anything to a file\n\n2 readFile will allow you to read all text from a file\n\n3 addToFile will allow you to add some text to the file\nDifferences:\nPython\n```python\nfile = open('name.txt', 'w')\nfile.write('Some text')\nfile.close()\n```\nFayouts\n```python\nwriteFile('name.txt', 'Some text')\n```\nPython\n```python\nfile = open('name.txt', 'r')\nprint(file.read())\nfile.close()\n```\nFayouts\n```python\nprint(readFile('name.txt'))\n```\n# Aiobot Module\nAttention! This module does not work correctly on versions below 1.0.3!\n\nSo far, the Aiobot module only allows you to create a template for the aiogram project, but soon there will be much more options. Unfortunately, it is impossible to guess exactly the structure of each bot, so my module creates just a simple template that everyone needs. I do not want to shove everything that is possible into this module at once, this is wrong, because this is how all customization disappears, all the opportunity to customize the bot for yourself.\n## Aiobot Docs\nTo create a project, you need to create a main.py file and write:\n```python\nimport fayouts.aiobot.startproject\n```\nYou can configure the bot in config.py, you must store all your filters in filters.py, and everything related to the bot itself in bot.py.\nbot.py is the entry point to your bot's program\n# Discobot Module\nThe Discobot module allows you to work with the Discord plugin to create discord bots.\n## Discobot Docs\nTo create a project, you need to create a main.py file and write:\n```python\nimport fayouts.discobot.startproject\n```\n\n# Fayouts Module\nversion 1.1.0+\n\nThe Fayouts module will allow you to create fields that persist even after the program is closed, you can refer to them by name from the Python code or from a .fy file.\n## Fayouts Docs\nFirst, you need to create a file with the extension .fy and any name, in my case it will be main.fy, create it near the file from which you will access it.\n\nNext, we need to initialize our fayout, this is done with the following line in the main.py file:\n```python\n# Connecting a module to work with fayouts\nfrom fayouts.fayouts.main import *\n\n# Fayout initialize\nmyfayout = Fayout('main')\n```\n\nAfter that, our fayout is ready to go. Let's get acquainted with its methods:\n\n```python\n# Create a new field\nmyfayout.New('Field Name', 'Field Content')\n\n# Reading an already created field\nprint(myfayout.Read('Field Name'))\n-> Field Content\n\n# Modifying an already created field\nmyfayout.Edit('Field Name', 'New Field Content')\n\n# Deleting an already created field by name\nmyfayout.Delete('Field Name')\n\n# Deleting the already created first field\nmyfayout.FPop()\n\n# Deleting an already created last field\nmyfayout.LPop()\n\n# Get the index of the field\nmyfayout.GetIndex('Field Name')\n```\n\nHow to work with fayout fields:\n\n1 You cannot create more than one field with the same name\n\n2 Can't read an uncreated field\n\n3 You cannot edit a field that has not yet been created.\n\n4 You cannot delete a field that has not yet been created.",
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
