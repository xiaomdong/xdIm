# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Wed Jan 05 08:57:38 2011
#      by: PySide uic UI code generator
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(224, 141)
        #pylint: disable=W0201
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.server_Label = QtGui.QLabel(Dialog)
        self.server_Label.setObjectName("server_Label")
        self.gridLayout.addWidget(self.server_Label, 0, 0, 1, 1)
        self.server_lineEdit = QtGui.QLineEdit(Dialog)
        self.server_lineEdit.setObjectName("server_lineEdit")
        self.gridLayout.addWidget(self.server_lineEdit, 0, 1, 1, 1)
        self.userLabel = QtGui.QLabel(Dialog)
        self.userLabel.setObjectName("userLabel")
        self.gridLayout.addWidget(self.userLabel, 1, 0, 1, 1)
        self.user_lineEdit = QtGui.QLineEdit(Dialog)
        self.user_lineEdit.setObjectName("user_lineEdit")
        self.gridLayout.addWidget(self.user_lineEdit, 1, 1, 1, 1)
        self.password_Label = QtGui.QLabel(Dialog)
        self.password_Label.setObjectName("password_Label")
        self.gridLayout.addWidget(self.password_Label, 2, 0, 1, 1)
        self.password_lineEdit = QtGui.QLineEdit(Dialog)
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.gridLayout.addWidget(self.password_lineEdit, 2, 1, 1, 1)
        self.ok_buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.ok_buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ok_buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.ok_buttonBox.setObjectName("ok_buttonBox")
        self.gridLayout.addWidget(self.ok_buttonBox, 3, 0, 1, 2)

        self.retranslateUi(Dialog)
#        QtCore.QObject.connect(self.ok_buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
#        QtCore.QObject.connect(self.ok_buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
#        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.server_Label.setText(QtGui.QApplication.translate("Dialog", "server", None, QtGui.QApplication.UnicodeUTF8))
        self.userLabel.setText(QtGui.QApplication.translate("Dialog", "user", None, QtGui.QApplication.UnicodeUTF8))
        self.password_Label.setText(QtGui.QApplication.translate("Dialog", "password", None, QtGui.QApplication.UnicodeUTF8))

