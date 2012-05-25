# -*- coding: utf-8 -*-
'''
Created on 2012-1-11

@author: x00163361
'''
from message_ui import Ui_MessageWindow
from PySide.QtGui import QMainWindow,QApplication
from PySide import QtCore
from debug import uiDebug

class messageWin(QMainWindow):
    def __init__(self,parent=None,user=None,friend=None):
        super(messageWin, self).__init__(parent)
        self.ui = Ui_MessageWindow()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.sendPushButton, QtCore.SIGNAL("clicked()"), self,QtCore.SLOT("sendMessage()"))
        self.friend=friend
        self.user=user
        
    def sendMessage(self):
        '''发送消息'''
#        message=self.ui.sendTextEdit.document().begin().text()
        message=self.ui.sendTextEdit.toPlainText()
        if message!="":
            self.ui.receTextEdit.append("you said: %s"%(message))
            print self.parent()
            print self.parent().connecting
            print self.parent().connecting.protocolInstance
            self.parent().connecting.protocolInstance.messageSend(self.friend,message)
            self.ui.sendTextEdit.clear()
            #还需要完成消息发送的调用
            
    def receMessage(self,message):
        '''接收消息'''
        if message!=None:
            self.ui.receTextEdit.append(message)

    def closeEvent(self,evt):
        '''关闭事件'''
        
        friend=self.windowTitle()
        del self.parent().messageFrame[friend]
        evt.accept()
        uiDebug("messageWin closeEvent")
                       
                
import sys      
def main():
    app=QApplication(sys.argv)
    app.setStyle("cleanlooks")
    im = messageWin()
    im.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()  
