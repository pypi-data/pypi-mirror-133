from spycalc.local import *

addLocalScope(__file__)

from extensions import *


from sympy import *
import sympy

from inspect import signature # for showing function parameters for LoadedFunctions

from PyQt5 import QtWidgets, uic

from os import getcwd, listdir
from os.path import dirname, abspath


# class wrapper for loaded_functions.ui
# shows all currently loaded extensions and parameters if available
class LoadedFunctions(QtWidgets.QDialog):
	def __init__(self, caller):
		super().__init__() # call parent constructor
		self.caller = caller # main window object
		uic.loadUi(getFilePath('loadedfunctions.ui', __file__), self) # load .ui file, and convert
		
		# excluded objects from being displayed
		self.exclude = ['__builtins__', '__cached__', '__doc__',
			'__file__', '__loader__', '__name__', '__package__',
			'__spec__', 'gmpy2', 'mpfr', 'mpnum', 'mpq', 'mpratio',
			'__path__'
		]

		# iterate through available extensions and call add_group on them
		for item in listdir(fileDir(__file__)+'/extensions'):
			if item.endswith('.py') and item != '__init__.py':
				self.add_group(item, eval(item[:-3]), excludes=dir(sympy))


		self.add_group('Advanced Math', sympy)

		self.listWidget.itemClicked.connect(lambda item: self.load_clicked_function(item))

		self.show()
	
	# add an extension and it's functions to self.listWidget using add_item
	def add_group(self, groupname, module, excludes=[]):
		self.add_item(' ------ ' + groupname + ' ------')
		for i in dir(module):
			if i not in self.exclude and i not in excludes:
				try:
					i += str(signature(eval(i)))
				except Exception:
					pass
				self.add_item(i)
	
	# used for list item click event
	# takes an item and adds it to calculator's current equation in main window
	def load_clicked_function(self, item):
		try:
			if self.caller.current_equ.text() == '' or not self.caller.current_equ.text().endswith(' '):
				self.caller.current_equ.setText(self.caller.current_equ.text()+' '+item.text())
			else:
				self.caller.current_equ.setText(self.caller.current_equ.text()+item.text())
		except AttributeError as e:
			print(' -- debug -- -> ' + str(e))
	
	# add an item to self.listWidget
	def add_item(self, name: str):
		self.listWidget.addItem(QtWidgets.QListWidgetItem(name))

