# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created: Mon Jan 09 14:01:18 2012
#      by: pyside-uic 0.2.13 running on PySide 1.0.9
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(180, 350)
        #pylint: disable=W0201
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.linkManTab = QtGui.QWidget()
        self.linkManTab.setObjectName("linkManTab")
        self.gridLayout_2 = QtGui.QGridLayout(self.linkManTab)
        self.gridLayout_2.setContentsMargins(1, 1, 1, 1)
        self.gridLayout_2.setSpacing(1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.linkManTreeView = QtGui.QTreeView(self.linkManTab)
        self.linkManTreeView.setObjectName("linkManTreeView")
        self.gridLayout_2.addWidget(self.linkManTreeView, 0, 0, 1, 1)
        self.tabWidget.addTab(self.linkManTab, "")
        self.groutTab = QtGui.QWidget()
        self.groutTab.setObjectName("groutTab")
        self.gridLayout_3 = QtGui.QGridLayout(self.groutTab)
        self.gridLayout_3.setContentsMargins(1, 1, 1, 1)
        self.gridLayout_3.setHorizontalSpacing(1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupTreeView = QtGui.QTreeView(self.groutTab)
        self.groupTreeView.setObjectName("groupTreeView")
        self.gridLayout_3.addWidget(self.groupTreeView, 0, 0, 1, 1)
        self.tabWidget.addTab(self.groutTab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 180, 18))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOption = QtGui.QMenu(self.menubar)
        self.menuOption.setObjectName("menuOption")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionLogin = QtGui.QAction(MainWindow)
        self.actionLogin.setObjectName("actionLogin")
        self.actionLogout = QtGui.QAction(MainWindow)
        self.actionLogout.setObjectName("actionLogout")
        self.actionAdd_friend = QtGui.QAction(MainWindow)
        self.actionAdd_friend.setObjectName("actionAdd_friend")
        self.actionDel_friend = QtGui.QAction(MainWindow)
        self.actionDel_friend.setObjectName("actionDel_friend")
        self.menuFile.addAction(self.actionLogin)
        self.menuFile.addAction(self.actionLogout)
        self.menuOption.addAction(self.actionAdd_friend)
        self.menuOption.addAction(self.actionDel_friend)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOption.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.linkManTab), QtGui.QApplication.translate("MainWindow", "Link man", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.groutTab), QtGui.QApplication.translate("MainWindow", "Group  ", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOption.setTitle(QtGui.QApplication.translate("MainWindow", "Operator", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLogin.setText(QtGui.QApplication.translate("MainWindow", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLogout.setText(QtGui.QApplication.translate("MainWindow", "Logout", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_friend.setText(QtGui.QApplication.translate("MainWindow", "Add friend", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDel_friend.setText(QtGui.QApplication.translate("MainWindow", "Del friend", None, QtGui.QApplication.UnicodeUTF8))

