from sys import path as syspath
import os.path as ospath

def addLocalScope(fileobj):
    syspath.append(ospath.dirname(__file__))

def getFilePath(filename, fileobj):
    return ospath.dirname(ospath.abspath(fileobj)) + '/' + filename

def fileDir(fileobj):
    return ospath.dirname(fileobj)