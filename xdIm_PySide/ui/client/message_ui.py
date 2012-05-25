# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'message.ui'
#
# Created: Wed Jan 11 08:49:30 2012
#      by: pyside-uic 0.2.13 running on PySide 1.0.9
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MessageWindow(object):
    def setupUi(self, MessageWindow):
        MessageWindow.setObjectName("MessageWindow")
        MessageWindow.resize(300, 350)
        #pylint: disable=W0201
        self.centralwidget = QtGui.QWidget(MessageWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.receTextEdit = QtGui.QTextEdit(self.centralwidget)
        self.receTextEdit.setObjectName("receTextEdit")
        self.gridLayout.addWidget(self.receTextEdit, 0, 0, 1, 3)
        self.clearPushButton = QtGui.QPushButton(self.centralwidget)
        self.clearPushButton.setAutoDefault(False)
        self.clearPushButton.setDefault(True)
        self.clearPushButton.setFlat(True)
        self.clearPushButton.setObjectName("clearPushButton")
        self.gridLayout.addWidget(self.clearPushButton, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(117, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.sendPushButton = QtGui.QPushButton(self.centralwidget)
        self.sendPushButton.setDefault(True)
        self.sendPushButton.setFlat(True)
        self.sendPushButton.setObjectName("sendPushButton")
        self.gridLayout.addWidget(self.sendPushButton, 1, 2, 1, 1)
        self.sendTextEdit = QtGui.QTextEdit(self.centralwidget)
        self.sendTextEdit.setObjectName("sendTextEdit")
        self.gridLayout.addWidget(self.sendTextEdit, 2, 0, 1, 3)
        MessageWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MessageWindow)
        QtCore.QMetaObject.connectSlotsByName(MessageWindow)

    def retranslateUi(self, MessageWindow):
        MessageWindow.setWindowTitle(QtGui.QApplication.translate("MessageWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.clearPushButton.setText(QtGui.QApplication.translate("MessageWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.sendPushButton.setText(QtGui.QApplication.translate("MessageWindow", "Send", None, QtGui.QApplication.UnicodeUTF8))

