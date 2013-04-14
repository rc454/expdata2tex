#!/usr/bin/python
# -*- coding: utf-8 -*-

# A simple GUI that emits experimental data as LaTeX
# Copyright (C) 2011 Russell Currie
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Please see the documentation under ./documentation/help.pdf

# To run, please run main.py

# You will need PyQt4, Qt4 and Python.

# Have Fun.

"""The UI"""
__version__ = "0.0.5"


import os, sys

# Import Qt modules
from PyQt4 import QtCore,QtGui, Qt

# Import the compiled UI module
from windowUi import Ui_MainWindow
from tex_popupUi import Ui_TexOut

import data_classes, shelve, custom_widgets, text_processing



def update_table(tableWidget, iterable_class):
	"""Maps a list of tuples into the table widget"""
	if iterable_class.__class__.__name__ == 'data_IR':
		# So that we dont end up with a rich text line edit for the IR as it isnt needed.
		for row in iterable_class:
			row_num = iterable_class.data.index(row)
			if tableWidget.rowCount() < (row_num+1):
				tableWidget.setRowCount(row_num+1)
			for column_num in range(0, len(row)):
				table_item = QtGui.QTableWidgetItem()
				table_item.setText(str(iterable_class.data[row_num][column_num]))
				tableWidget.setItem(row_num, column_num, table_item)
	else:
		for row in iterable_class:
			row_num = iterable_class.data.index(row)
			if tableWidget.rowCount() < (row_num+1):
				tableWidget.setRowCount(row_num+1)
			for column_num in range(0, len(row)):
				if column_num == (len(row)-1): # This is for the highlightlineedits
					table_item = custom_widgets.HighlightTextLineEdit()
					table_item.insertHtml(str(iterable_class.data[row_num][column_num]))
					tableWidget.setCellWidget(row_num, column_num, table_item)
				else:
					table_item = QtGui.QTableWidgetItem()
					table_item.setText(str(iterable_class.data[row_num][column_num]))
					tableWidget.setItem(row_num, column_num, table_item)
def check_nonetype(item):
	"""For table items. Checks if they are NoneType, if not, returns the text they contain."""
	if item is None:
		text = ""
	elif item.__class__.__name__ == 'HighlightTextLineEdit':
		text = item.toHtml()
	else: text = item.text()
	return text



# Create a class for our main window
class Main(QtGui.QMainWindow, Ui_MainWindow):
	# Create the mother object for data storage
	save_path=''
	save_filename=''
	nmr_solvents = {'Chloroform-d1':'CDCl3', 'Acetic Acid-d4': 'AcOD-d4', 'Acetone-d6': 'Me2C=O-d6', 'Acetonitrile-d3': 'MeCN-d6', 'Benzene-d6': 'C6D6', 'DCM-d2': 'CD2Cl2', 'DMF-d7': 'DMF-d7', 'DMSO-d6': 'DMSO-d6', 'Ethanol-d6': 'EtOD-d6', 'Methanol-d4': 'MeOD-d4', 'Nitromethane-d3': 'MeNO2-d3', 'Pyridine-d5': 'C5D5N', 'TFA-d1': 'CF3COOD', 'THF-d8': 'THF-d8', 'Toluene-d8': 'PhMe-d8', 'Trifluoroethanol-d3': 'CF3CH22OD', 'Water-d2': 'D2O'}
	nmr_solvent_index = ['Chloroform-d1', 'Acetic Acid-d4', 'Acetone-d6', 'Acetonitrile-d3', 'Benzene-d6', 'DCM-d2', 'DMF-d7', 'DMSO-d6', 'Ethanol-d6', 'Methanol-d4', 'Nitromethane-d3', 'Pyridine-d5', 'TFA-d1', 'THF-d8', 'Toluene-d8', 'Trifluoroethanol-d3', 'Water-d2']
	def __init__(self):
		QtGui.QMainWindow.__init__(self)

		# This is always the same
		self.ui=Ui_MainWindow()
		self.ui.setupUi(self)
		
		# The save files
		self.save_path = os.path.join(os.getcwd(), '.tmp')
		self.save_filename = os.path.join(self.save_path, 'data.db')
		
		
		#global all_Data
		self.all_Data = data_classes.mother()
		
		# Connect up Signals
		# Actions
		self.ui.actionNew.triggered.connect(self.fileNew)
		self.ui.actionOpen.triggered.connect(self.load_data)
		self.ui.actionSave.triggered.connect(self.save_data)
		self.ui.actionSave_As.triggered.connect(self.save_as)
		self.ui.actionExit.triggered.connect(self.exit)
		self.ui.actionAdd_Row.triggered.connect(self.add_row)
		self.ui.actionRemove_Row.triggered.connect(self.remove_row)
		self.ui.actionCompile.triggered.connect(self.compile_to_tex)
		self.ui.actionHelp.triggered.connect(self.openHelp)
		self.ui.actionAbout.triggered.connect(self.about)
		self.ui.tableWidget_proton.currentCellChanged.connect(self.count_protons) # Count the number of protons whenever a cell is changed
		
		self.fileNew() # Start with a new file
		
	def about(self):
		QtGui.QMessageBox.about(self, 'About', 'expdata2tex: Converts experimental data to LaTex. See documentation (F1) for full information')
	def openHelp(self):
		helpfile = os.path.join('.', 'documentation', 'help.pdf')
		if sys.platform.startswith('darwin'):
			os.system('open %s' %helpfile)
		elif sys.platform.startswith('linux'):
			os.system('xdg-open %s' %helpfile)
		elif sys.platform.startswith('win32'):
			os.system('start %s' %helpfile)
	def set_table_widget(self):
		# Make the far right cell into a highlighttextlineedit
		self.ui.tableWidget_proton.setCellWidget((self.ui.tableWidget_proton.rowCount()-1), 4,
		custom_widgets.HighlightTextLineEdit())
		self.ui.tableWidget_carbon.setCellWidget((self.ui.tableWidget_carbon.rowCount()-1), 1, custom_widgets.HighlightTextLineEdit())

	def fileNew(self):
		self.ui.lineEdit_specificrotation.setText("0.0")
		self.ui.lineEdit_concentration.setText("0.0")
		self.ui.lineEdit_solvent.setText("CHCl3")
		self.ui.tableWidget_proton.clearContents()
		self.ui.tableWidget_carbon.clearContents()
		self.ui.tableWidget_IR.clearContents()
		self.ui.tableWidget_IR.setRowCount(1) # Start off with one row in each
		self.ui.tableWidget_carbon.setRowCount(1)
		self.ui.tableWidget_proton.setRowCount(1)
		self.set_table_widget()
		# Set the window title to a new file
		self.setWindowTitle('%s' %('Experimental Data to Latex (expdata2tex): ' + 'Untitled'))
		
		# Count the number of protons, and update 
		self.count_protons()
		
	def rsave(self):
		if os.path.isdir(self.save_path)==False:
			os.makedirs(self.save_path)
		self.update_data()
		f = open(self.save_filename, 'wb')
		for obj in self.all_Data:
			if obj.__class__.__name__ == 'AD':
				f.write('++++AD++++')
				f.write(repr(obj))
				f.write('\n')
			if obj.__class__.__name__ == 'data_IR':
				f.write('++++IR++++')
				f.write(obj.toString())
				f.write('\n')
			if obj.__class__.__name__ == 'proton_specinfo':
				f.write('++++HINFO++++')
				f.write(repr(obj))
				f.write('\n')
			if obj.__class__.__name__ == 'proton_data':
				f.write('++++HDATA++++')
				f.write(obj.toString())
				f.write('\n')
			if obj.__class__.__name__ == 'carbon_specinfo':
				f.write('++++CINFO++++')
				f.write(repr(obj))
				f.write('\n')
			if obj.__class__.__name__ == 'carbon_data':
				f.write('++++CDATA++++')
				f.write(obj.toString())
				f.write('\n')
		f.close()
		
		# Update the title
		self.update_title()
		
	def save_data(self): # Change from this to XML
		if os.path.isdir(self.save_path)==False:
			os.makedirs(self.save_path)
		self.update_data()

		print 'savedata filename', self.save_filename
		#s.close()
		self.rsave()
	def update_title(self):
		# Updates the window title
		self.setWindowTitle('%s' %('Experimental Data to Latex (expdata2tex): ' + os.path.split(self.save_filename)[-1]))
	def save_as(self):
		fname = unicode(QtGui.QFileDialog.getSaveFileName(self, "SaveAs ", self.save_filename, "Any File (*.*)"))
		self.save_filename = fname
		self.save_data()

	
	def load_data(self):
		self.all_Data = self.load_file()
		self.update_gui()
		self.update_title()
	def load_file(self):
		fname = unicode(QtGui.QFileDialog.getOpenFileName(self, "Open ", self.save_filename, "Any File (*.*)"))
		if fname != u'':
			self.save_filename = fname
			f = open(self.save_filename, 'rb')
			data_lines = f.readlines()
			f.close()
			for line in data_lines:
				line=line.strip('\n') # Remove the newlines

				if line[:10] == '++++AD++++':
					(_rotation, _concentration, _solvent) = tuple(line[10:].split(','))
					self.all_Data._AD.insert(_rotation, _concentration, _solvent)
				if line[:10] == '++++IR++++':
					self.all_Data._data_IR.fromString(line[10:])
				if line[:13] == '++++HINFO++++':
					(self.all_Data._proton_specinfo.proton_frequency, self.all_Data._proton_specinfo.proton_solvent) = tuple(line[13:].split(','))
				if line[:13] =='++++HDATA++++':
					self.all_Data._proton_data.fromString(line[13:]) # Need to sort out identity column
				if line[:13] == '++++CINFO++++':
					(self.all_Data._carbon_specinfo.carbon_frequency, self.all_Data._carbon_specinfo.carbon_solvent) = tuple(line[13:].split(','))
				if line[:13] =='++++CDATA++++':
					self.all_Data._carbon_data.fromString(line[13:]) # Need to sort out identity column
			self.update_gui()
		
		
		return self.all_Data
		
	def update_gui(self):
		# The AD Stuff
		self.ui.lineEdit_specificrotation.setText('%s' %self.all_Data._AD.data[0])
		self.ui.lineEdit_concentration.setText('%s' %self.all_Data._AD.data[1])
		self.ui.lineEdit_solvent.setText('%s' %self.all_Data._AD.data[2])
		
		# The IR stuff
		update_table(self.ui.tableWidget_IR, self.all_Data._data_IR)
		
		# The Carbon stuff
		update_table(self.ui.tableWidget_carbon, self.all_Data._carbon_data)
		
		self.ui.comboBox_carbonsolvent.setCurrentIndex(self.nmr_solvent_index.index(str(self.all_Data._carbon_specinfo.carbon_solvent)))
		self.ui.lineEdit_carbonfrequency.setText(QtCore.QString('%s' %self.all_Data._carbon_specinfo.carbon_frequency))
		
		# The Proton stuff
		update_table(self.ui.tableWidget_proton, self.all_Data._proton_data)
		
		self.ui.comboBox_protonsolvent.setCurrentIndex(self.nmr_solvent_index.index(str(self.all_Data._proton_specinfo.proton_solvent)))
		self.ui.lineEdit_frequency.setText(QtCore.QString('%s' %self.all_Data._proton_specinfo.proton_frequency))
		
		# Count the number of protons, and update 
		self.count_protons()
		
	def update_data(self):
		# Update the alpha D values
		self.all_Data._AD.insert(str(self.ui.lineEdit_specificrotation.text()), str(self.ui.lineEdit_concentration.text()), str(self.ui.lineEdit_solvent.text()))
		# The IR data
		if (self.ui.tableWidget_IR.rowCount() < len(self.all_Data._data_IR)):
			# This is a check. If the user deletes rows, they will need to be deleted from the data class.
			difference = (len(self.all_Data._data_IR) - self.ui.tableWidget_IR.rowCount())
			for index in range(0, -difference, -1):
				del self.all_Data._data_IR.data[index]
				
		for row in range(0, self.ui.tableWidget_IR.rowCount()):
			item0 = self.ui.tableWidget_IR.item(row, 0)
			text0 = check_nonetype(item0)
			
			item1 = self.ui.tableWidget_IR.item(row, 1)
			text1 = check_nonetype(item1)
			self.all_Data._data_IR.add_update(row, str(text0), str(text1))
		
		# The carbon data
		
		self.all_Data._carbon_specinfo.carbon_frequency = self.ui.lineEdit_carbonfrequency.text()
		self.all_Data._carbon_specinfo.carbon_solvent = self.ui.comboBox_carbonsolvent.currentText()
		
		if (self.ui.tableWidget_carbon.rowCount() < len(self.all_Data._carbon_data)):
			# This is a check. If the user deletes rows, they will need to be deleted from the data class.
			difference = (len(self.all_Data._carbon_data) - self.ui.tableWidget_carbon.rowCount())
			for index in range(0, -difference, -1):
				del self.all_Data._carbon_data.data[index]
		for row in range(0, self.ui.tableWidget_carbon.rowCount()):
			item0 = self.ui.tableWidget_carbon.item(row, 0)
			text0 = check_nonetype(item0)
			
			item1 = self.ui.tableWidget_carbon.cellWidget(row, 1)
			text1 = check_nonetype(item1)
			self.all_Data._carbon_data.add_update(row, str(text0), str(text1).replace('\n',''))
		
		#The proton data_classes
		self.all_Data._proton_specinfo.proton_frequency = self.ui.lineEdit_frequency.text()
		self.all_Data._proton_specinfo.proton_solvent = self.ui.comboBox_protonsolvent.currentText()

		if (self.ui.tableWidget_proton.rowCount() < len(self.all_Data._proton_data)):
			# This is a check. If the user deletes rows, they will need to be deleted from the data class.
			difference = (len(self.all_Data._proton_data) - self.ui.tableWidget_proton.rowCount())
			for index in range(0, -difference, -1):
				del self.all_Data._proton_data.data[index]
		for row in range(0, self.ui.tableWidget_proton.rowCount()):
			item0 = self.ui.tableWidget_proton.item(row, 0)
			text0 = check_nonetype(item0)
			item1 = self.ui.tableWidget_proton.item(row, 1)
			text1 = check_nonetype(item1)
			item2 = self.ui.tableWidget_proton.item(row, 2)
			text2 = check_nonetype(item2)
			item3 = self.ui.tableWidget_proton.item(row, 3)
			text3 = check_nonetype(item3)
			item4 = self.ui.tableWidget_proton.cellWidget(row, 4)
			text4 = check_nonetype(item4)
			self.all_Data._proton_data.add_update(row, str(text0), str(text1), str(text2), str(text3), str(text4).replace('\n',''))
			
			
	def count_protons(self):
		"""Count the number of protons in the table widget"""
		proton_count = 0
		for row in range(0, self.ui.tableWidget_proton.rowCount()):
			item = self.ui.tableWidget_proton.item(row, 1)
			if item != None:
				proton_count += int(self.ui.tableWidget_proton.item(row, 1).text())
		self.ui.num_protons.setText(str(proton_count))

	def add_row(self):
		#Check which tab is active, then add a row for that widget
		
		# Proton Tab
		if self.ui.Data_Tabs.currentIndex() == 0:
			row_num = self.ui.tableWidget_proton.currentRow() +1 # If no rows exist, the row num is -1, so add 1 to bring the row index to -0
			self.ui.tableWidget_proton.insertRow(row_num)
			self.ui.tableWidget_proton.setCellWidget(row_num, 4, custom_widgets.HighlightTextLineEdit()) # Make the last cell a highlighttextedit
		if self.ui.Data_Tabs.currentIndex() == 1:
			row_num = self.ui.tableWidget_carbon.currentRow() +1
			self.ui.tableWidget_carbon.insertRow(row_num)
			self.ui.tableWidget_carbon.setCellWidget(row_num, 1, custom_widgets.HighlightTextLineEdit())# Make the last cell a highlighttextedit
		if self.ui.Data_Tabs.currentIndex() == 2:
			row_num = self.ui.tableWidget_IR.currentRow() +1
			self.ui.tableWidget_IR.insertRow(row_num)
		
	def remove_row(self):
		if self.ui.Data_Tabs.currentIndex() == 0:
			row_num = self.ui.tableWidget_proton.currentRow()
			self.ui.tableWidget_proton.removeRow(row_num)
		if self.ui.Data_Tabs.currentIndex() == 1:
			row_num = self.ui.tableWidget_carbon.currentRow()
			self.ui.tableWidget_carbon.removeRow(row_num)
		if self.ui.Data_Tabs.currentIndex() == 2:
			row_num = self.ui.tableWidget_IR.currentRow()
			self.ui.tableWidget_IR.removeRow(row_num)
	def make_tex(self):
		self.update_data() # Update the data classes
		output_string = '' # This is the complete string that will be displayed
		# The AD Stuff
		if (str(self.all_Data._AD.data[0]) != '0.0') and (str(self.all_Data._AD.data[1]) != '0.0'):
			output_string +=  '\\alphad = $%s$ (c= %s, \\ce{%s}); ' %(self.all_Data._AD.data[0], self.all_Data._AD.data[1], self.all_Data._AD.data[2])
		
		# The IR Stuff
		if self.all_Data._data_IR.isEmpty() == False:
			output_string += 'IR'
			for item in self.all_Data._data_IR:
				output_string += ' %s (%s),' %item
			output_string = output_string[:-1] + '; '
		
		# The Proton stuff
		if self.all_Data._proton_data.isEmpty() == False:
			output_string += '\\HNMR NMR (%s \mega\hertz, \ce{%s}, 300 K)' %(self.all_Data._proton_specinfo.proton_frequency, self.nmr_solvents[str(self.all_Data._proton_specinfo.proton_solvent)])
			for item in self.all_Data._proton_data:
				(a, b, c, d, e) = (item[0], item[1], item[2], item[3], text_processing.description_to_tex(text_processing.to_sensible_html(item[4])))
				if d != '' and e != '\\ce{}}':
					output_string += ' $\\delta$~%s (%sH, %s, \JNMR{%s}, %s)' %(a, b, c, d, e) + ',' 
				elif (d == '') and (e != '\\ce{}}'):
					output_string += ' $\\delta$~%s (%sH, %s, %s)' %(a, b, c, e) + ',' 
				elif (d != '') and (e == '\\ce{}}'):
					output_string += ' $\\delta$~%s (%sH, %s, \JNMR{%s})' %(a, b, c, d) + ',' 
			output_string = output_string[:-1]+'; '
		
		# The Carbon stuff
		if self.all_Data._carbon_data.isEmpty() == False:
			output_string += '\\CNMR NMR (%s \mega\hertz, \ce{%s}, 300 K)' %(self.all_Data._carbon_specinfo.carbon_frequency, self.nmr_solvents[str(self.all_Data._carbon_specinfo.carbon_solvent)])
			for item in self.all_Data._carbon_data:
				output_string += ' $\\delta$~%s (%s)' %(item[0], text_processing.description_to_tex(text_processing.to_sensible_html(item[1]))) + ','
		output_string = output_string[:-1]+'.'
		return output_string

	def compile_to_tex(self):
		self.dialog = QtGui.QDialog()
		self.dialog.ui = Ui_TexOut()
		self.dialog.ui.setupUi(self.dialog)
		self.dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		text = self.make_tex()
		self.dialog.ui.textBrowser.setText(text)
		self.dialog.exec_()
		
	def exit(self):
		sys.exit(0)

def main():


	app = QtGui.QApplication(sys.argv)
	window=Main()
	window.show()
		# It's exec_ because exec is a reserved word in Python
	sys.exit(app.exec_())
	

# Start the main loop
if __name__ == "__main__":
	main()
