from importlib import import_module
from os import listdir

# from sys import path as syspath
from os import path as ospath


# !!!!!   The stack overflow guy said that this was dangerous
for item in listdir(ospath.dirname(__file__)):
    if item.endswith('.py') and item != '__init__.py':
        item = item[:-3]
        module = import_module('extensions.'+item).__dict__
        try:
            to_import = module.__all__
        except AttributeError:
            to_import = [name for name in module if not name.startswith('_')]
        globals().update({name: module[name] for name in to_import})
