# -*- coding: utf-8 -*-
'''
Created on 2012-1-11

@author: x00163361
'''
#import sys
from login_ui import Ui_Dialog
from  PySide import QtCore
#from PySide.QtGui import QApplication
from debug import uiDebug
from PySide.QtGui import QDialog

#app = QApplication(sys.argv)
#import qt4reactor
#qt4reactor.install()
#from twisted.internet import reactor
#from protocol.client import client_twisted

class loginDialog(QDialog):
    def __init__(self, parent=None):
#        QDialog.__init__(self)
        super(loginDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
#        QObject.connect(self.ui.openXml_pushButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("xml_open()"))
        QtCore.QObject.connect(self.ui.ok_buttonBox, QtCore.SIGNAL("accepted()"), self,QtCore.SLOT("onAccepted()"))
        QtCore.QObject.connect(self.ui.ok_buttonBox, QtCore.SIGNAL("rejected()"), self,QtCore.SLOT("onRejected()"))
        self.connecting=None
        self.parent=parent

    def onAccepted(self):
        '''确定动作'''
        host=str(self.ui.server_lineEdit.text())
        port=8002
        user=str(self.ui.user_lineEdit.text())
        password=str(self.ui.password_lineEdit.text())
        uiDebug("host: "+host+",user: "+user+",password: "+password)
        self.parent.connectServer(host,port,user,password)
        uiDebug("loginPanelUi onAccepted()")

    def onRejected(self):
        '''取消动作'''
        self.parent.closeEvent()
        self.reject()
        uiDebug("loginPanelUi onRejected()")
 
    def closeEvent(self,evt):
        uiDebug("loginPanelUi closeEvent() start")
        self.parent.closeEvent(evt)      
        uiDebug("loginPanelUi closeEvent() end")
      
#def main():
#    app.setStyle("cleanlooks")
#    im = loginDialog("test")
#    im.show()
#    sys.exit(app.exec_())
##    reactor.run()
#
#if __name__ == '__main__':
#    main()  
#                        