'''
Created on 2010-12-8

@author: x00163361
'''

from ui.im.loginPanel_xrc import *
#from protocol.client import client_twisted
#from config import *
from debug import uiDebug

class loginPanel(xrcmainPanel):
    def __init__(self, parent):
        self.parent=parent
        xrcmainPanel.__init__(self, parent)
        self.mainPanel = xrc.XRCCTRL(self, "mainPanel")
        self.serverStaticText = xrc.XRCCTRL(self, "serverStaticText")
        self.serverComboBox = xrc.XRCCTRL(self, "serverComboBox")
        self.userStaticText = xrc.XRCCTRL(self, "userStaticText")
        self.userComboBox = xrc.XRCCTRL(self, "userComboBox")
        self.passwordStaticText = xrc.XRCCTRL(self, "passwordStaticText")
        self.passwordTextCtrl=xrc.XRCCTRL(self, "passwordTextCtrl")
        self.okButton = xrc.XRCCTRL(self, "okButton")
        self.cancelButton = xrc.XRCCTRL(self, "cancelButton") 
        
        try:
            self.textencoding = getTextCoding()
        except:
            self.textencoding = None  
            
    def handleSuccess(self, result, port):
        uiDebug( "loginPanelUi handleSuccess")
        uiDebug(result)
        self.parent.updatePanel()
         
    
    
    def handelFailure(self, failure, port):
        uiDebug( "loginPanelUi handelFailure")
        uiDebug(failure.getErrorMessage())
        try:
            message=unicode(failure.getErrorMessage(), self.textencoding)
        except:
            message="Something is Err!"
        dlg = wx.MessageDialog(None, message,
                               "A Message Box",
                               wx.YES_NO )
        dlg.ShowModal()

         

    #!XRCED:begin-block:xrcmainPanel.OnButton_okButton
    def OnButton_okButton(self, evt):
        # Replace with event handler code
        host=str(self.serverComboBox.GetValue())
        port=8002
        user=str(self.userComboBox.GetValue())
        password=str(self.passwordTextCtrl.GetLabel())
        password=str(self.passwordTextCtrl.GetValue())
        uiDebug("password:"+user+"password:"+password)
        self.parent.connectServer(host,port,user,password,self.handleSuccess,self.handelFailure)
        uiDebug("loginPanelUi OnButton_okButton()")
#!XRCED:end-block:xrcmainPanel.OnButton_okButton        

#!XRCED:begin-block:xrcmainPanel.OnButton_cancelButton
    def OnButton_cancelButton(self, evt):
        # Replace with event handler code
#        self.parent.updatePanel()
                
        uiDebug("loginPanelUi OnButton_cancelButton()")
#!XRCED:end-block:xrcmainPanel.OnButton_cancelButton   