# -*- coding: utf-8 -*-
#!/usr/bin/python
from PyQt4 import Qt, QtCore, QtGui
import platform

class HighlightTextLineEdit(Qt.QTextEdit):
	def __init__(self, parent=None):
		super(HighlightTextLineEdit, self).__init__(parent)
		self.setLineWrapMode(Qt.QTextEdit.NoWrap) # No wrapping, line edit
		
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) # No Scroll bars
		self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		
		self.setTabChangesFocus(True) # So we dont insert a tab character
		
		fontm = Qt.QFontMetrics(self.font()) # The font metrics
		self.setToolTip("Press <b>Ctrl+U</b> to highlight portion")
		# Size isnt set, so that it occupies the cell.
		
	def keyPressEvent(self, event):
		if event.modifiers() & QtCore.Qt.ControlModifier:
			event_handled = False
			if event.key() == QtCore.Qt.Key_U:
				self.toggleUnderline()
				event_handled = True
			if event_handled:
				event.accept()
				return
		if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
			self.emit(QtCore.SIGNAL("returnPressed()"))			
			event.accept()
		else:
			QtGui.QTextEdit.keyPressEvent(self, event)
	
	def toggleUnderline(self):
		self.setFontUnderline(not self.fontUnderline())
	def __repr__(self):
		return self.toHtml
