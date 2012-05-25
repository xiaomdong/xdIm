# -*- coding: utf-8 -*-
'''
Created on 2012-1-9

@author: x00163361
'''

import sys
from PySide.QtGui import QApplication

app = QApplication(sys.argv)
import qt4reactor
qt4reactor.install()



from twisted.internet import reactor
from ui.client.login import loginDialog
#from ui.client.message import messageWin
from ui.client.client import  client
from protocol.client import client_twisted

from debug import uiDebug

class im(client):
    #pylint: disable=W0621 
    def __init__(self,app,parent=None):
        super(im, self).__init__(parent)
        self.login=loginDialog(self)
        self.login.show()
        self.mainPanel=self
        self.app=app
        self.connecting=None
        self.user=""
        self.friends=[]
        self.taskBar=None
        
    def setUserFriends(self,friends):
        '''设置用户Friends 由客户端协议调用'''
        uiDebug("im setUserFriends start")
        self.friends=friends    
        uiDebug("im setUserFriends end")

    def connectServer(self,host,port,user,password):
        '''连接服务器,由login界面登录时调用'''
        self.user=user
        client_twisted.frame = self
        self.connecting=client_twisted.clientMain(host,port,user,password)
        uiDebug( "connectServer")
        
    def updatePanel(self):
        '''登录服务器成功后，更新用户界面，由客户端协议调用'''
        uiDebug("updatePanel start")
        uiDebug(self.friends)
        self.login.hide()
        self.show()
        self.login.destroy()
        del self.login
        self.createFriendList()
            
        uiDebug("updatePanel end")

    def createFriendList(self):
        '''创建主窗口的联系人列表'''
        if self.friends!=None:
            for friend in self.friends:
                uiDebug("* "+friend)    
                if friend!="":
                    self.mainPanel.addLinkMan(friend,"linked")
        uiDebug("createFriendList end")           
    
    #pylint: disable=W0613 
    def closeEvent(self,evt=None):
        '''关闭事件'''
        uiDebug("parent closeEvent")
        #pylint: disable=E1101 
        reactor.stop()
        self.app.exit()
        uiDebug("parent closeEvent end")
       

    def refreshReceMessage(self,src,dst,message):
        '''收到服务器的消息时，更新消息接收文本框'''
        if self.mainPanel.messageFrame.has_key(src):
            pass
        else:
            #如果没有窗口，重新创建窗口
            self.mainPanel.createTempMessageFrame(self.user,src)
            
        try: 
            self.mainPanel.messageFrame[src].receMessage(message)
            #pylint: disable=W0702                 
        except:
            uiDebug("im refreshReceMessage error " + src +" " +dst)

               
                   
def main():
#    app=QApplication(sys.argv)
    app.setStyle("cleanlooks")
    d = im(app)
    client_twisted.clientUi=d
    #pylint: disable=E1101 
    reactor.run()

if __name__ == '__main__':
    main()  
                    
