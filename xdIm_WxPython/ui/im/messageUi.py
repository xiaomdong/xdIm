# -*- coding: UTF-8 -*-
'''
Created on 2010-12-22

@author: x00163361
'''

from ui.im.message_xrc import *
from config import *
from debug import uiDebug


class messageFrame(xrcclientFrame):
    def __init__(self, parent,user,friend):
        xrcclientFrame.__init__(self, parent)

        self.user=user
        self.friend=friend
        self.mainPanel = xrc.XRCCTRL(self, "mainPanel")
        self.receMesPanel = xrc.XRCCTRL(self, "receMesPanel")
        self.receMessageText = xrc.XRCCTRL(self, "receMessageText")
        
        self.sendMesPanel = xrc.XRCCTRL(self, "sendMesPanel")
        self.sendMesTool = xrc.XRCCTRL(self, "sendMesTool")
        self.copyTool = xrc.XRCCTRL(self, "copyTool")
        self.pasteTool=xrc.XRCCTRL(self, "pasteTool")
        self.sendTool = xrc.XRCCTRL(self, "sendTool")
        self.sendMessageText = xrc.XRCCTRL(self, "sendMessageText")
        self.SetTitle(friend)
                
        try:
            self.textencoding = getTextCoding()
        except:
            self.textencoding = None  
            
#!XRCED:begin-block:xrcclientFrame.OnClose
    def OnClose(self, evt):
        # Replace with event handler code
#        print self.Parent
#        print self.Parent.messageFrame[self.friend]
        del self.Parent.messageFrame[self.friend]
        self.Destroy()
        uiDebug("messageUi OnClose()")
#!XRCED:end-block:xrcclientFrame.OnClose   


##!XRCED:begin-block:xrcclientFrame.OnTool_sendTool
#    def OnTool_sendTool(self, evt):
#        # Replace with event handler code
#        msg=self.sendMessageText.GetValue()
#        data="mesS desS %s desE souS %s souE conS %s conE mesE\r\n"%(str(self.friend),str(self.user),str(msg))
#        self.Parent.Parent.connecting.protocolInstance.dataSend(data)
#        self.sendMessageText.Clear()
#        print "OnTool_sendTool()"
##!XRCED:end-block:xrcclientFrame.OnTool_sendTool   


#!XRCED:begin-block:xrcclientFrame.OnTool_sendTool
    def OnTool_sendTool(self, evt):
        # Replace with event handler code
        msg=self.sendMessageText.GetValue()
        if msg=="":
            return
        if self.friend != self.user :
#            data=u"mesS desS %s desE souS %s souE conS %s conE mesE\r\n"%(self.friend,self.user,msg)
#            self.Parent.Parent.connecting.protocolInstance.dataSend(data)
#            data=u"mesS desS %s desE souS %s souE conS %s conE mesE\r\n"%(self.friend,self.user,msg)
            self.Parent.Parent.connecting.protocolInstance.messageSend(self.friend,self.user,msg)
            self.sendMessageText.Clear()
            self.receMessageText.AppendText("\n"+"you said: "+msg)
        else:
            self.receMessageText.AppendText("\n"+"you said: "+msg)
            self.sendMessageText.Clear()
            pass    
        uiDebug("messageUi OnTool_sendTool()")
#!XRCED:end-block:xrcclientFrame.OnTool_sendTool   
            
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = messageFrame(None)
    frame.Show()
    app.MainLoop()

  