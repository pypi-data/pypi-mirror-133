from sys import path as syspath # allow appending python search path
import os.path as ospath # utilities for handling path to current file directory

## fileobj will usually be __file__ from whatever script is calling it

# add current file location's parent directory to python search path
def addLocalScope(fileobj):
    syspath.append(ospath.dirname(__file__))

# get absolute path of file relative to location of fileobj
def getFilePath(filename, fileobj):
    return ospath.dirname(ospath.abspath(fileobj)) + '/' + filename

# get parent directory of fileobj
def fileDir(fileobj):
    return ospath.dirname(fileobj)