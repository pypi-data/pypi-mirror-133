#!/usr/bin/python3


from sys import argv
from os import getcwd, system
from os.path import dirname, abspath
from webbrowser import open_new
import os

# imports for PyQt5
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt




from loaded import *
from update import UpdateWindow

import sympy

# dirname(abspath(__file__))+fname


# class wrapper for loading .ui file
class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__() # call parent constructor
		uic.loadUi(dirname(abspath(__file__))+'/main.ui', self) # load .ui file, and convert

		self.inputs = []
		self.pindex = -1

		# set numeric button press values
		# pass value to a lambda function of button_clicked
		self.zero.clicked.connect(lambda: self.button_clicked(0))
		self.one.clicked.connect(lambda: self.button_clicked(1))
		self.two.clicked.connect(lambda: self.button_clicked(2))
		self.three.clicked.connect(lambda: self.button_clicked(3))
		self.four.clicked.connect(lambda: self.button_clicked(4))
		self.five.clicked.connect(lambda: self.button_clicked(5))
		self.six.clicked.connect(lambda: self.button_clicked(6))
		self.seven.clicked.connect(lambda: self.button_clicked(7))
		self.eight.clicked.connect(lambda: self.button_clicked(8))
		self.nine.clicked.connect(lambda: self.button_clicked(9))

		# set numeric focus policies
		self.zero.setFocusPolicy(Qt.NoFocus)
		self.one.setFocusPolicy(Qt.NoFocus)
		self.two.setFocusPolicy(Qt.NoFocus)
		self.three.setFocusPolicy(Qt.NoFocus)
		self.four.setFocusPolicy(Qt.NoFocus)
		self.five.setFocusPolicy(Qt.NoFocus)
		self.six.setFocusPolicy(Qt.NoFocus)
		self.seven.setFocusPolicy(Qt.NoFocus)
		self.eight.setFocusPolicy(Qt.NoFocus)
		self.nine.setFocusPolicy(Qt.NoFocus)

		# set operation buttons
		self.add.clicked.connect(lambda: self.button_clicked('+'))
		self.min.clicked.connect(lambda: self.button_clicked('-'))
		self.mul.clicked.connect(lambda: self.button_clicked('*'))
		self.div.clicked.connect(lambda: self.button_clicked('/'))
		self.sqrt.clicked.connect(lambda: self.button_clicked('sqrt('))

		# set operation focus policies
		self.add.setFocusPolicy(Qt.NoFocus)
		self.min.setFocusPolicy(Qt.NoFocus)
		self.mul.setFocusPolicy(Qt.NoFocus)
		self.div.setFocusPolicy(Qt.NoFocus)
		self.sqrt.setFocusPolicy(Qt.NoFocus)

		# set etc. buttons and other actions
		self.clear.clicked.connect(self.clear_list)
		self.equ.clicked.connect(self.evaluate)
		self.current_equ.returnPressed.connect(self.evaluate)
		self.back.clicked.connect(self.backspace)
		self.prev.clicked.connect(self.load_prev_equ)
		self.next.clicked.connect(self.load_next_equ)

		# set misc. focus policies
		self.clear.setFocusPolicy(Qt.NoFocus)
		self.equ.setFocusPolicy(Qt.NoFocus)
		self.back.setFocusPolicy(Qt.NoFocus)
		self.prev.setFocusPolicy(Qt.NoFocus)
		self.next.setFocusPolicy(Qt.NoFocus)

		# set menu action
		self.action_Exit.triggered.connect(lambda: exit(0))
		self.actionLoaded_Scripts.triggered.connect(lambda: LoadedFunctions(self).exec())
		self.action_Help.triggered.connect(lambda: open_new('file://'+getFilePath('docs.html', __file__)))
		self.action_Update.triggered.connect(lambda: UpdateWindow().exec())

		# add list click behavior
		self.prev_out.itemClicked.connect(lambda item: self.get_item_clicked(item))

		self.show() # show the window

	# set the focus back to the current equation for more seemless usage between buttons and typing
	def reset_focus(self):
		self.current_equ.setFocus()
	
	def get_item_clicked(self, item):
		if item.text() != 'error':
			self.current_equ.setText(self.current_equ.text()+item.text())
		self.reset_focus()
	
	# remove list item -1
	def backspace(self):
		try:
			self.current_equ.setText(self.current_equ.text().replace(self.current_equ.text()[-1], '', 1))
		except Exception:
			pass
		self.reset_focus()
	
	# copy the previous equation into current equation by decrementing pindex
	def load_prev_equ(self):
		try:
			self.pindex -= 1
			if self.pindex < 0:
				self.pindex = 0
			self.current_equ.setText(self.inputs[self.pindex])
		except IndexError:
			self.pindex += len(self.inputs)
		self.reset_focus()
	
	# copy the next most recent equation by incrementing pindex
	def load_next_equ(self):
		try:
			self.pindex += 1
			if self.pindex >= len(self.inputs):
				self.pindex = len(self.inputs)-1
			self.current_equ.setText(self.inputs[self.pindex])
		except IndexError:
			self.pindex -= 2
		self.reset_focus()

	# standard number pad button click handler
	def button_clicked(self, value):
		if type(value) != type('example'):
			value = str(value)
		self.current_equ.setText(self.current_equ.text()+value)
		self.reset_focus()
	
	# evaluate function to parse and execute equations as python code
	def evaluate(self):
		if self.current_equ.text() == 'clear':
			self.current_equ.setText('')
			self.prev_out.clear()
			return
		elif self.current_equ.text() == 'exit':
			exit(0)
		output = None
		intext = self.current_equ.text()
		intext.replace('^', '**', -1)
		self.inputs.append(intext)
		self.pindex = len(self.inputs)
		try:
			tmp = sympy.sympify(intext).evalf()
			if type(tmp) != type(sympify('sqrt(2)').evalf()):
				raise Exception
			else:
				output = str(tmp)
		except Exception as e:
			try:
				output = str(eval(intext))
			except Exception as e:
				print(e)
				output = "error"
		finally:
			if output != None and output != 'None':
				self.prev_out.addItem(QtWidgets.QListWidgetItem(output))

		self.current_equ.setText('')
		self.reset_focus()
	
	# clear the list items
	def clear_list(self):
		if self.current_equ.text() != '':
			self.current_equ.setText('')
		else:
			self.prev_out.clear()
			self.inputs = []
			self.pindex = -1
		self.reset_focus()
	
	# custom close event to close mainwindow and all dialogs
	def closeEvent(self, event):
		exit(0)



if __name__ == '__main__':
	app = QtWidgets.QApplication(argv) # load the command line arguments
	window = MainWindow() # create window instance of our main window class
	window.current_equ.setFocus()
	app.exec_() # run the qt app
