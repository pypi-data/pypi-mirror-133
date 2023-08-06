# Datetime Module
Datetime allows you to work with the current date and time. It adds only one function, and it allows you to get the date and time. Datetime is based on your PC's time zone.
## Datetime Docs
First, you need to call the getData () function, which is called without parameters, then in square brackets you should indicate what you want to get, for example minutes.
```python
1| print(getData()['minutes'])
31
1| print(getData()['year'])
2022
1| print(getData()['dateUs'])
03.01.2022
1| print(getData)['weekday']
Monday
```

# Start Module
The Start Module allows you to create a new Python project, it creates a whole tree, including files, folders for source files, and so on. The module is called by a single import in a python file.
## Start Docs
1 Create a folder with the name of your project

2 Create a main.py file in the root of the folder

3 In the file, write the following command
```python 
1| import fayouts.start.newproject
```
4 Run the main.py file, after creating the project, delete it

# Files Module
The Files module lets you work with files much easier than in the original Python.
# Files Docs
Functions
1 writeFile will let you write anything to a file

2 readFile will allow you to read all text from a file

3 addToFile will allow you to add some text to the file
Differences:
Python
```python
file = open('name.txt', 'w')
file.write('Some text')
file.close()
```
Fayouts
```python
writeFile('name.txt', 'Some text')
```
Python
```python
file = open('name.txt', 'r')
print(file.read())
file.close()
```
Fayouts
```python
print(readFile('name.txt'))
```
# Aiobot Module
So far, the Aiobot module only allows you to create a template for the aiogram project, but soon there will be much more options. Unfortunately, it is impossible to guess exactly the structure of each bot, so my module creates just a simple template that everyone needs. I do not want to shove everything that is possible into this module at once, this is wrong, because this is how all customization disappears, all the opportunity to customize the bot for yourself.
## Aiobot Docs
To create a project, you need to create a main.py file and write:
```python
import fayouts.aiobot.startproject
```
You can configure the bot in config.py, you must store all your filters in filters.py, and everything related to the bot itself in bot.py.
bot.py is the entry point to your bot's program