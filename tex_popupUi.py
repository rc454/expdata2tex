# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './tex_popup.ui'
#
# Created: Mon Jan 16 22:56:20 2012
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TexOut(object):
    def setupUi(self, TexOut):
        TexOut.setObjectName("TexOut")
        TexOut.resize(480, 641)
        self.verticalLayout = QtGui.QVBoxLayout(TexOut)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtGui.QFrame(TexOut)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textBrowser = QtGui.QTextBrowser(self.frame)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtGui.QDialogButtonBox(TexOut)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(TexOut)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), TexOut.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), TexOut.reject)
        QtCore.QMetaObject.connectSlotsByName(TexOut)

    def retranslateUi(self, TexOut):
        TexOut.setWindowTitle(QtGui.QApplication.translate("TexOut", "LaTeX", None, QtGui.QApplication.UnicodeUTF8))

