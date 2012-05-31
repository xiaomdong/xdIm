# -*- coding: utf-8 -*-
'''
pyside-uic serverManager.ui -o serverManager_ui.py

pyside-lupdate serverManager_ui.py -ts serverManager.ts

lrelease serverManager.ts serverManagerAdd.ts -qm serverManager.qm

Created on 2011-1-8

@author: x00163361
'''

import sys

from debug import uiDebug  



from PySide.QtGui import QMainWindow, QStandardItemModel , QStandardItem , QFileDialog, QApplication, QMessageBox, QAction, QDesktopWidget
from PySide.QtCore import QObject , Qt  , QDir , QTranslator, SIGNAL, SLOT 
from PySide.QtGui import QSystemTrayIcon, QIcon, QMenu
#from PySide.QtCore import QEvent, QTimer

import qt4reactor
app = QApplication(sys.argv)
qt4reactor.install()
from twisted.internet import reactor

from ui.server.serverManager_ui import Ui_MainWindow
from protocol.server import server_twisted

from config import serverConfig, mediaValue
#from debug import *
from control.txt.txtUserControl import txtUserControl
from control.xml.xmlUserControl import xmlUserControl
from control.sqlite.sqliteUserControl import sqliteUserControl
#from control.mysql.mysqlUserControl import mysqlUserControl



configFile = ".\server.cfg"
chineseLanguageFile = ".\serverManager.qm"
Chinese = "Chinese"
English = "English"
txt = "txt"
xml = "xml"
mysql = "MySQL"
sqlite = "Sqlite"


#class userTableView(QAbstractTableModel):
#    
#    def rowCount(self,parent=QModelIndex()):
#        return 3
#        pass 
#  
#    def columnCount(self,parent=QModelIndex()):
#        return 3
#        pass 
#   
#    def data(self,index,role):
#        return "xd"
#        pass
#
#    def headerData(self, section, orientation, role):
#        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
#            if section == 0:
#                return "Name"
#
#            if section == 1:
#                return "Attributes"
#
#            if section == 2:
#                return "Value"
#
#        return None


class serverManagerWindow(QMainWindow):
    def __init__(self, _app, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.iTrayIcon = QSystemTrayIcon()
        self.iTrayIcon.setIcon(QIcon("drapes.ico"))
        self.iTrayIcon.show()
        self.iTrayIcon.setToolTip("One world, One dream!")
        self.iTrayIcon.activated.connect(self.iconActivated)
        self.quitAction = QAction("&Quit", self, triggered=QApplication.quit)
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)
        self.iTrayIcon.setContextMenu(self.trayIconMenu)

        #选择MYSQL保留用户信息
        QObject.connect(self.ui.mysql_groupBox, SIGNAL("clicked()"), self, SLOT("choiceSql()"))
        #选择XT文件留用户信息
        QObject.connect(self.ui.text_groupBox, SIGNAL("clicked()"), self, SLOT("choiceTxt()"))
        #选择XML文件留用户信息
        QObject.connect(self.ui.xml_groupBox, SIGNAL("clicked()"), self, SLOT("choiceXml()"))                
        #节面显示英文
        QObject.connect(self.ui.actionEnglish, SIGNAL("activated()"), self, SLOT("loadEnglish()"))
        #节面显示中文
        QObject.connect(self.ui.actionChinese, SIGNAL("activated()"), self, SLOT("loadChinese()"))
        
        #加载配置文件
        QObject.connect(self.ui.actionLoad_Config, SIGNAL("activated()"), self, SLOT("loadConfig()"))
        #保留配置文件
        QObject.connect(self.ui.actionSave_Config, SIGNAL("activated()"), self, SLOT("saveConfig()"))
        #about操作
        QObject.connect(self.ui.actionAbout, SIGNAL("activated()"), self, SLOT("about()"))
        
        #选择XML文件
        QObject.connect(self.ui.openXml_pushButton, SIGNAL("clicked()"), self, SLOT("xml_open()"))
        #选择TXT文件
        QObject.connect(self.ui.openText_pushButton, SIGNAL("clicked()"), self, SLOT("txt_open()"))
        #启动服务
        QObject.connect(self.ui.startServer_pushButton, SIGNAL("clicked()"), self, SLOT("startServer()"))
        #停止服务
        QObject.connect(self.ui.stopServer_pushButton, SIGNAL("clicked()"), self, SLOT("stopServer()"))

        self.ui.sqlTypeComboBox.activated[str].connect(self.sqlServer)
                
        QObject.connect(self.ui.openSqlpushButton, SIGNAL("clicked()"), self, SLOT("database_open()"))
        

        #界面语言
        self.translator = None
        self.app = _app
        self.translator = QTranslator() 
        self.connect = None
        self.users = None
        self.ControlMediaPath = None
        self.ControlMedia = None
        self.delUsrInfo = None

        self.userModel = QStandardItemModel()
        self.userModel.setHorizontalHeaderItem(0, QStandardItem("user"))
        self.userModel.setHorizontalHeaderItem(1, QStandardItem("friends"))
        

        self.userModel.setVerticalHeaderItem(0, QStandardItem("1"))
        self.userModel.setVerticalHeaderItem(1, QStandardItem("2"))
        self.userModel.setVerticalHeaderItem(2, QStandardItem("3"))

        self.loginUserModel = QStandardItemModel()
        self.loginUserModel.setHorizontalHeaderItem(0, QStandardItem("user"))
        self.loginUserModel.setHorizontalHeaderItem(1, QStandardItem("instance"))
        
        self.messageModel = QStandardItemModel()
        self.messageModel.setHorizontalHeaderItem(0, QStandardItem("message"))

        #读取系统配置文件
        self.readConfig(configFile)
        self.statusBar().showMessage("server is stopped!")
        
        self.ui.userInfo_tableView.setModel(self.userModel)
        self.createUserInfoContextMenu()
        self.ui.loginUsers_tableView.setModel(self.loginUserModel)
        self.createloginUsersContextMenu()
        self.ui.messageLogs_listView.setModel(self.messageModel)

        #界面多语处理
        self.updateLanguage(self.language)
        
        self.center()
        
    def iconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
        print "iconActivated"
    
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        print "closeEvent"

#    def changeEvent(self,event):
#        if (event.type() == QEvent.WindowStateChange) and (self.isMinimized()):
#            QTimer.singleShot(100, self, SLOT("close"))
#            
#        print "changeEvent"    
                
    def sqlServer(self, index):
        if index == "MySQL":
            self.ui.openSqlpushButton.setDisabled(True)
            self.ui.userLineEdit.setEnabled(True)
            self.ui.passwordlineEdit.setEnabled(True)        
            
        if  index == "Sqlite":
            self.ui.openSqlpushButton.setEnabled(True)
            self.ui.userLineEdit.setDisabled(True)
            self.ui.passwordlineEdit.setDisabled(True)        
        
    def center(self):  
        screen = QDesktopWidget().screenGeometry()  
        size = self.geometry()  
        self.move((screen.width() - size.width()) / 2,
            (screen.height() - size.height()) / 2)  
        
    def createUserInfoContextMenu(self):
        '''添加用户信息快捷菜单'''
        #pylint: disable=W0201
        self.addUserAct = QAction(self)
#        self.addUserAct.setText("add User")
        
        self.delUserAct = QAction(self)
#        self.delUserAct.setText("del User")

        self.undoDelUserAct = QAction(self)
#        self.undoDelUserAct.setText("undo del User")
        
        self.saveDataRowAct = QAction(self)
#        self.saveDataRowAct.setText("save Data")
        
        self.ui.userInfo_tableView.addAction(self.addUserAct)
        self.ui.userInfo_tableView.addAction(self.delUserAct)
        self.ui.userInfo_tableView.addAction(self.undoDelUserAct)
        self.ui.userInfo_tableView.addAction(self.saveDataRowAct)
        
        QObject.connect(self.addUserAct, SIGNAL("activated()"), self, SLOT("userInfoAddRow()"))
        QObject.connect(self.delUserAct, SIGNAL("activated()"), self, SLOT("userInfoDelRow()"))
        QObject.connect(self.undoDelUserAct, SIGNAL("activated()"), self, SLOT("userInfoUndoDelRow()"))        
        QObject.connect(self.saveDataRowAct, SIGNAL("activated()"), self, SLOT("userInfoSaveData()"))
        
        self.ui.userInfo_tableView.setContextMenuPolicy(Qt.ActionsContextMenu)

    
    def userInfoAddRow(self):
        '''添加一条用户数据'''
#        self.userModel.appendRow(QStandardItem(""))
        index = self.ui.userInfo_tableView.selectionModel().currentIndex()
        model = self.ui.userInfo_tableView.model()

        if not model.insertRow(index.row() + 1, index.parent()):
            return

        for column in range(model.columnCount(index.parent())):
            child = model.index(index.row() + 1, column, index.parent())
            model.setData(child, "[No data]", Qt.EditRole)
            
        uiDebug("userInfoAddRow")
    

    def userInfoDelRow(self):
        '''删除数据，且保留此次删除的数据'''
        model = self.ui.userInfo_tableView.model()
        index = self.ui.userInfo_tableView.selectionModel().currentIndex()
        user = model.item(index.row(), 0).index().data()
        friendlist = model.item(index.row(), 1).index().data()
        self.delUsrInfo = [index.row(), user, friendlist]
#        print self.delUsrInfo
        try:
            model.removeRow(index.row(), index.parent())
            self.users.deleteUser(user)
            self.users.userDataSave()
            #pylint: disable=W0702 
        except:    
            pass        
        uiDebug("userInfoDelRow")        

    def userInfoUndoDelRow(self):
        '''恢复前次删除的数据'''
        if self.delUsrInfo != None:
            model = self.ui.userInfo_tableView.model()
            if not model.insertRow(self.delUsrInfo[0]):
                return
            user = self.delUsrInfo[1]
            friendlist = self.delUsrInfo[2]      
            self.userModel.setItem(self.delUsrInfo[0], 0, QStandardItem(user))
            self.userModel.setItem(self.delUsrInfo[0], 1, QStandardItem(friendlist))
            if user != "[No data]":
                self.users.addUser(user, "admin")
            if friendlist != "[No data]":    
                for friend in friendlist.split(","):            
                    self.users.addUserFriend(user, friend)
            self.users.userDataSave()    
        self.delUsrInfo = None        
        uiDebug("userInfoUndoDelRow")


    def userInfoSaveData(self):
        '''保留用户数据'''
        if self.users:
            model = self.ui.userInfo_tableView.model()
            index = self.ui.userInfo_tableView.selectionModel().currentIndex()
            for row in range(model.rowCount(index.parent())):
                user = model.item(row, 0).index().data()
                friendlist = model.item(row, 1).index().data()
                if user != "[No data]":
                    self.users.addUser(user, "admin")
                if friendlist != "[No data]":
                    for friend in friendlist.split(","):
                        if friend != '':
                            self.users.addUserFriend(user, friend)   
        
            self.users.userDataSave()
            self.clearUserInfo()    
            self.showUserinfo()
        uiDebug("userInfoSaveData")        
    

    def showConfig(self):
        '''显示配置'''
#        print self.Config.getControlMedia()    
#        print self.Config.getControlMediaPath()   
#        print self.ControlMedia
#        print self.ControlMediaPath     
        self.ui.information_textBrowser.setText("Control Media: " + self.ControlMedia)
        self.ui.information_textBrowser.append("Control Media path: " + self.ControlMediaPath)

    def showUserinfo(self):
        '''显示用户信息'''
        userlist = self.users.getUsers()
        print "showUserinfo "
        print userlist
        row = 0
        for user in userlist:
            friends = userlist[user]
            self.userModel.setItem(row, 0, QStandardItem(user))
            self.userModel.setItem(row, 1, QStandardItem(friends))
            row = row + 1  
        #pylint: disable=W0201    
        self.delUsrInfo = None
    
    def clearUserInfo(self):
        '''清除用户信息'''
        self.userModel.clear()
        self.delUsrInfo = None

        
    def userConfig(self):
        self.showConfig()
        if self.users != None:
            del self.users        
        #服务器配置
        if self.ControlMedia == mediaValue[txt]:
            #txt文件保留用户信息
            self.users = txtUserControl(self.ControlMediaPath)
            self.ui.text_groupBox.setChecked(True)
            self.ui.text_lineEdit.setText(self.ControlMediaPath)
        elif self.ControlMedia == mediaValue[xml]:
            #xml文件保留用户信息
            self.users = xmlUserControl(self.ControlMediaPath)
            self.ui.xml_groupBox.setChecked(True)
            self.ui.xml_lineEdit.setText(self.ControlMediaPath)
            
        elif self.ControlMedia == mediaValue[mysql]:
            #mysql数据库保留用户信息   
            self.ui.mysql_groupBox.setChecked(True)
            self.ui.ServerLineEdit.setText(self.ControlMediaPath)
            self.ui.sqlTypeComboBox.setCurrentIndex(0)
#            print "mysql" 
            self.sqlServer(mysql)    
        elif self.ControlMedia == mediaValue[sqlite]:
            self.ui.mysql_groupBox.setChecked(True)
            self.ui.ServerLineEdit.setText(self.ControlMediaPath)
            self.ui.sqlTypeComboBox.setCurrentIndex(1)
            self.users = sqliteUserControl(self.ControlMediaPath)
            self.sqlServer(sqlite)
#            print "sqlite"
            
        #用户数据初始化
            
        try:     
            self.users.userDataInit()
#            self.showUserinfo()
            #pylint: disable=W0702
        except:
            self.users = None

        if self.users != None:
            self.clearUserInfo()
            self.showUserinfo()
                    
    def readConfig(self, _file):
        '''读取服务器端配置文件'''
        #pylint: disable=W0201
        self.Config = serverConfig(_file)
        self.ControlMedia = self.Config.getControlMedia() 
        self.ControlMediaPath = self.Config.getControlMediaPath()        
        self.language = self.Config.getLanguage()
        self.userConfig()
        uiDebug("readConfig")
                    
    def startServer(self):
        '''#启动服务'''
        self.ui.startServer_pushButton.setEnabled(False)
        self.ui.stopServer_pushButton.setEnabled(True)
        self.connect = server_twisted.serverMain(8002, self.users)
        self.saveConfig()
#        self.readConfig(configFile)
        self.userConfig()
        self.ui.mysql_groupBox.setDisabled(True)
        self.ui.text_groupBox.setDisabled(True)
        self.ui.xml_groupBox.setDisabled(True)
        self.statusBar().showMessage("server is starting!")
        
        if self.users != None:
            self.clearUserInfo()
            self.showUserinfo()
        uiDebug("startServer")

    def stopServer(self):
        ''' #停止服务'''
        if self.connect != None:
            self.ui.startServer_pushButton.setEnabled(True)
            self.ui.stopServer_pushButton.setEnabled(False)
            self.ui.mysql_groupBox.setDisabled(False)
            self.ui.text_groupBox.setDisabled(False)
            self.ui.xml_groupBox.setDisabled(False)  
            #pylint: disable=E1101          
            reactor.disconnectAll()
#            self.clearUserInfo()
            self.statusBar().showMessage("server is stopped!")
        uiDebug("stopServer")
        

    def loadChinese(self):
        '''加载中文'''
        self.updateLanguage(Chinese)

    def loadEnglish(self):
        '''加载英文'''
        self.updateLanguage(English)
        
    def updateLanguage(self, language):
        '''设置界面语言'''
        if self.translator != None:
            self.app.removeTranslator(self.translator)
            
        if language == Chinese:
            #中文处理
            self.translator.load(chineseLanguageFile)
            self.app.installTranslator(self.translator)  
            self.Config.setLanguage(Chinese)
        elif language == English:
            #英文处理
            self.Config.setLanguage(English)   
        else:
            pass
    
        #更新界面
        self.retranslateUi()
        #保留配置
        self.Config.saveServerConfig()
        
            
    def txt_open(self):
        self.fileOpen(self.ui.text_lineEdit, txt)
        
    def xml_open(self):
        self.fileOpen(self.ui.xml_lineEdit, xml)

    def database_open(self):
        self.fileOpen(self.ui.ServerLineEdit, mysql)

    def fileOpen(self, lineEdit, filters):
        openFile = QFileDialog.getOpenFileName(self, "Find Files", QDir.currentPath(), filters="*." + filters)
        uiDebug(openFile)
        if openFile != None :
            lineEdit.setText(openFile[0])
            self.setUserConfig()
            self.showConfig()
                    
    def choiceSql(self):
        uiDebug("choiceMysql")
        self.ui.text_groupBox.setChecked(False)
        self.ui.xml_groupBox.setChecked(False)
        if  self.ui.sqlTypeComboBox.currentText() == mysql:
            self.ui.openSqlpushButton.setDisabled(True)
            self.ui.userLineEdit.setEnabled(True)
            self.ui.passwordlineEdit.setEnabled(True)   
            
        if  self.ui.sqlTypeComboBox.currentText() == sqlite:
            self.ui.openSqlpushButton.setEnabled(True)
            self.ui.userLineEdit.setDisabled(True)
            self.ui.passwordlineEdit.setDisabled(True)
            
    def choiceTxt(self):
        uiDebug("choiceTxt")
        self.ui.mysql_groupBox.setChecked(False)
        self.ui.xml_groupBox.setChecked(False)

    def choiceXml(self):
        uiDebug("choiceXml")
        self.ui.mysql_groupBox.setChecked(False)
        self.ui.text_groupBox.setChecked(False)

    def setUserConfig(self):
        '''保留用户配置'''
        if self.ui.xml_groupBox.isChecked() == True:
            if self.ui.xml_lineEdit.text() != "":
                self.ControlMedia = xml
                self.ControlMediaPath = self.ui.xml_lineEdit.text()
                uiDebug("setUserConfig xml: " + xml)
         
        if self.ui.text_groupBox.isChecked() == True:
            if self.ui.text_lineEdit.text() != "":
                self.ControlMedia = txt
                self.ControlMediaPath = self.ui.text_lineEdit.text()
                uiDebug("setUserConfig txt: " + txt)
         
        if self.ui.mysql_groupBox.isChecked() == True:
            if self.ui.sqlTypeComboBox.currentText() == mysql:
                self.ControlMedia = mysql
                uiDebug("setUserConfig mysql: " + mysql)
            if self.ui.sqlTypeComboBox.currentText() == sqlite:
                self.ControlMedia = sqlite
                uiDebug("setUserConfig sqlite: " + sqlite)
            self.ControlMediaPath = self.ui.ServerLineEdit.text()

        self.Config.setContrlMedia(self.ControlMedia)
        self.Config.setControlMediaPath(self.ControlMediaPath)
        self.userConfig()    
        
    def createloginUsersContextMenu(self):
        '''添加登陆用户快捷菜单'''
        #pylint: disable=W0201
        self.killUserAct = QAction(self)
#        self.killUserAct.setText("kill user")
        
        self.messageUserAct = QAction(self)
#        self.messageUserAct.setText("message user")
        
        self.ui.loginUsers_tableView.addAction(self.killUserAct)
        self.ui.loginUsers_tableView.addAction(self.messageUserAct)
        
        QObject.connect(self.killUserAct, SIGNAL("activated()"), self, SLOT("killUser()"))
        QObject.connect(self.messageUserAct, SIGNAL("activated()"), self, SLOT("messageUser()"))
        
        self.ui.loginUsers_tableView.setContextMenuPolicy(Qt.ActionsContextMenu)

    def killUser(self):
        '''踢出一个用户'''
        try:
            index = self.ui.loginUsers_tableView.selectionModel().currentIndex()
            model = self.ui.loginUsers_tableView.model()
            user = model.item(index.row(), 0).index().data()
            self.connect.killUser(user)
            #pylint: disable=W0702
        except:
            pass    
#        model.removeRow(index.row(), index.parent())
        uiDebug("killUser")

    def messageUser(self):
        '''发送消息给用户'''
        uiDebug("messageUser")        
    
    def addUsers(self, user, instance):
        '''添加一条登陆用户数据'''

        index = self.ui.loginUsers_tableView.selectionModel().currentIndex()
        model = self.ui.loginUsers_tableView.model()
        row = model.rowCount(index.parent())
        model.setItem(row, 0, QStandardItem(user))
        model.setItem(row, 1, QStandardItem(str(instance)))
        
        uiDebug("loginUser")
    
    def removeUser(self, user):
        '''删除一条登陆用户数据'''
        index = self.ui.loginUsers_tableView.selectionModel().currentIndex()
        model = self.ui.loginUsers_tableView.model()
        maxRow = model.rowCount(index.parent())
#        print user
        for row in range(maxRow):
#            print row
#            print model.item(row, 0).index().data()
#            print type(model.item(row, 0).index().data())
            if user == model.item(row, 0).index().data():
                model.removeRow(row, index.parent())                             
                
        uiDebug("logoutUser")

    def refreshReceMessage(self, message):
        '''添加接收信息'''
        model = self.ui.messageLogs_listView.model()
#        model.setItem(model.rowCount(),QStandardItem(message))
        model.appendRow(QStandardItem(message))
        uiDebug("refreshReceMessage")        

    def refreshSendMessage(self, message):
        '''添加发送信息'''
        model = self.ui.messageLogs_listView.model()
#        model.setItem(model.rowCount(),QStandardItem(message))
        model.appendRow(QStandardItem(message))
        uiDebug("refreshSendMessage")        

    def retranslateUi(self):
        self.addUserAct.setText(QApplication.translate("MainWindow", "add User", None, QApplication.UnicodeUTF8))
        self.delUserAct.setText(QApplication.translate("MainWindow", "del User", None, QApplication.UnicodeUTF8))
        self.undoDelUserAct.setText(QApplication.translate("MainWindow", "undo del  User", None, QApplication.UnicodeUTF8))
        self.saveDataRowAct.setText(QApplication.translate("MainWindow", "save Data", None, QApplication.UnicodeUTF8))
        self.killUserAct.setText(QApplication.translate("MainWindow", "kill User", None, QApplication.UnicodeUTF8))
        self.messageUserAct.setText(QApplication.translate("MainWindow", "message User", None, QApplication.UnicodeUTF8))
        self.quitAction.setText(QApplication.translate("MainWindow", "Quit", None, QApplication.UnicodeUTF8))
        self.iTrayIcon.setToolTip(QApplication.translate("MainWindow", "One world, One dream!", None, QApplication.UnicodeUTF8))
        
        self.ui.retranslateUi(self)

    def loadConfig(self):
        '''加载配置文件'''
        configfile = QFileDialog.getOpenFileName(self, "Load Config File", QDir.currentPath(), filter="*.cfg")
        uiDebug(configfile)
        if configfile != None :
            self.readConfig(configfile)
            self.stopServer()
            self.startServer()
            self.showConfig()
        uiDebug("loadConfig") 

    def saveConfig(self):
        '''保留配置文件'''
        self.setUserConfig()
        self.Config.saveServerConfig()
        uiDebug("saveConfig") 

    def about(self):
        '''about'''
        aboutInfo = '''<HTML>
         <p>xdIm ver 0.2.0</p>
         <p>xdIm program is a software program by xd.</p>
         <p>Copy Right : "(C) 2008-2010 Programmers and Coders Everywhere"</p>
         <p><a href="http://www.xdIm.org/">http://www.xdIm.org</a></p>
         </HTML>"'''
         
        tranAboutInfo = QApplication.translate("MainWindow", aboutInfo, None, QApplication.UnicodeUTF8)
        QMessageBox.information(self, "xdIm information", tranAboutInfo)
        uiDebug("about") 
                                             
def main():
#    app=QApplication(sys.argv)
    app.setStyle("cleanlooks")
#    app.setStyle("arthurStyle")
    d = serverManagerWindow(app)
    server_twisted.frame = d
    d.show()
#    reactor.run()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()            
    
    
