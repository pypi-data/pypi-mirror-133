import os

def newFolder(name):
    try:
        os.mkdir(name)
    except FileExistsError:
        print('Такая папка уже есть!')

def writeFile(name, content):
    file = open(name, 'w', encoding='utf-8')
    file.write(content)
    file.close()

def readFile(name):
    file = open(name, 'r', encoding='utf-8')
    returning = file.read()
    file.close()
    return returning

def addToFile(name, content):
    file = open(name, 'a', encoding='utf-8')
    file.write(content)
    file.close()