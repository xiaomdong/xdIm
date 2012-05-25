# -*- coding: utf-8 -*-
'''
Created on 2012-1-11

@author: x00163361

注意事项：
在__init__(self,parent = None)函数中实现
self.parent=parent

需要定义def closeEvent(self,event):在其中调用
其中parent需要提供closeEvent(),以在窗口关闭时使用
'''

from client_ui import Ui_MainWindow
#from clientData import friendModel,friendItem
from message import messageWin
from PySide import QtCore
from PySide.QtGui import QMainWindow, QApplication, QStandardItemModel,QStandardItem
from debug import uiDebug
#from twisted.internet import reactor

class client(QMainWindow):   
    def __init__(self,parent= None):
#        QMainWindow.__init__(self)
        super(client, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.userModel = QStandardItemModel()
        self.itemHeadFriend=QStandardItem()
        self.itemHeadFriend.setData("linkMan",QtCore.Qt.DisplayRole)
        self.itemHeadStatis=QStandardItem()
        self.itemHeadStatis.setData("status",QtCore.Qt.DisplayRole)
        self.userModel.setHorizontalHeaderItem(0,self.itemHeadFriend)
        self.userModel.setHorizontalHeaderItem(1,self.itemHeadStatis)

                
        self.itemFriend=QStandardItem()
        self.itemFriend.setData("friend",QtCore.Qt.DisplayRole)
        self.userModel.insertRow(0,self.itemFriend)
        self.ui.linkManTreeView.setModel(self.userModel)

        self.connecting=None
        QtCore.QObject.connect(self.ui.linkManTreeView, QtCore.SIGNAL("clicked(QModelIndex)"), self,QtCore.SLOT("createMessageFrame(QModelIndex)"))
        self.messageFrame={}



    def addLinkMan(self,linkMan,status):
        '''添加联系人'''
        itemLinkMan=QStandardItem()
        itemLinkMan.setData(linkMan,QtCore.Qt.DisplayRole)
        itemLinkManStatus=QStandardItem()
        itemLinkManStatus.setData(status,QtCore.Qt.DisplayRole)

        self.itemFriend.appendRow([itemLinkMan,itemLinkManStatus])

    def createTempMessageFrame(self,user,friend):
        uiDebug(self.messageFrame)
        if self.messageFrame.has_key(friend):
            self.messageFrame[friend].show()
        else:    
            try:        
                frame = messageWin(self,user,friend)
                frame.setWindowTitle(friend)
                self.messageFrame[friend]=frame
                frame.show()
                #pylint: disable=W0702 
            except:
                pass
        
        uiDebug("mainPanelUi createMessageFrame()")
        
    
    def createMessageFrame(self,QModelIndex):
        '''创建对话窗口'''
        friend= self.userModel.data(QModelIndex)

        if self.userModel.indexFromItem(self.itemFriend) == QModelIndex:
            return
        
        if friend == "":
            return
        
        if friend == "inline":
            return
        
        uiDebug(self.messageFrame)
        if self.messageFrame.has_key(friend):
            self.messageFrame[friend].show()
        else:    
            try:        
                frame = messageWin(self,self.user,friend)
                frame.setWindowTitle(friend)
                self.messageFrame[friend]=frame
                frame.show()
                #pylint: disable=W0702 
            except:
                pass
        
        uiDebug("mainPanelUi createMessageFrame()")
      
import sys      
def main():
    app=QApplication(sys.argv)
    app.setStyle("cleanlooks")
    im = client()
    im.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()  
