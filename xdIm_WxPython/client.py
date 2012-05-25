# -*- coding: UTF-8 -*-
from debug import *
from twisted.internet import wxreactor
wxreactor.install()
from twisted.internet import reactor, defer


from ui.client.client_xrc import *
from protocol.client import client_twisted

global clientConnector

class client(xrcclientFrame):
    def __init__(self,parent):
        xrcclientFrame.__init__(self,parent)
        self.clientFrame=xrc.XRCCTRL(self,"clientFrame")
        self.mainPanel=xrc.XRCCTRL(self,"mainPanel")

        self.serDataPanel=xrc.XRCCTRL(self,"serDataPanel")
        self.ServerText=xrc.XRCCTRL(self.serDataPanel,"serverText")
        self.UserText=xrc.XRCCTRL(self.serDataPanel,"userText")
        self.passwordText=xrc.XRCCTRL(self.serDataPanel,"passwordText")
        self.serverTextCtrl=xrc.XRCCTRL(self.serDataPanel,"serverTextCtrl")
        self.userTextCtrl=xrc.XRCCTRL(self.serDataPanel,"userTextCtrl")
        self.passwordTextCtrl=xrc.XRCCTRL(self.serDataPanel,"passwordTextCtrl")

        self.recMesPanel=xrc.XRCCTRL(self.mainPanel,"receMesPanel")
        self.receMessageText=xrc.XRCCTRL(self.recMesPanel,"receMessageText")

        self.senMesPanel=xrc.XRCCTRL(self.mainPanel,"sendMesPanel")
        self.sendMesTool=xrc.XRCCTRL(self.senMesPanel,"sendMesTool")
        self.copy=xrc.XRCCTRL(self.sendMesTool,"copyTool")
        self.paste=xrc.XRCCTRL(self.sendMesTool,"pasteTool")
        self.send=xrc.XRCCTRL(self.sendMesTool,"sendTool")
        self.friendText=xrc.XRCCTRL(self.sendMesTool,"friendText")
        self.friendTextCtrl=xrc.XRCCTRL(self.sendMesTool,"friendTextCtrl")
        self.sendMessageText=xrc.XRCCTRL(self.senMesPanel,"sendMessageText")

        self.mainToolBar=xrc.XRCCTRL(self,"mainToolBar")
        self.connectTool=xrc.XRCCTRL(self.mainToolBar,"connectTool")
        self.loseconnectTool=xrc.XRCCTRL(self.mainToolBar,"loseconnectTool")
        self.closeTool=xrc.XRCCTRL(self.mainToolBar,"closeTool")
        self.statusText=xrc.XRCCTRL(self.mainToolBar,"statusText")
        
        # Define variables for the controls, bind event handlers

#        self.Bind(wx.EVT_TOOL, self.OnTool_copyTool, id=xrc.XRCID('copyTool'))
#        self.Bind(wx.EVT_TOOL, self.OnTool_pasteTool, id=xrc.XRCID('pasteTool'))
#        self.Bind(wx.EVT_TOOL, self.OnTool_sendTool, id=xrc.XRCID('sendTool'))
#        self.Bind(wx.EVT_KEY_DOWN, self.OnKey_down_sendMessageText, id=xrc.XRCID('sendMessageText'))
#        self.Bind(wx.EVT_TOOL, self.OnTool_connectTool, id=xrc.XRCID('connectTool'))
#        self.Bind(wx.EVT_TOOL, self.OnTool_loseconnectTool, id=xrc.XRCID('loseconnectTool'))
#        self.Bind(wx.EVT_TOOL, self.OnTool_closeTool, id=xrc.XRCID('closeTool'))
        
        
#!XRCED:begin-block:xrcclientFrame.OnTool_send
    def OnTool_sendTool(self, evt):
        # Replace with event handler code
        printdebug("OnTool_sendTool()")
        #self.transport.write("mesS desS xd desE souS cvs souE conS welcomexd conE mesE\r\n")
        friend=self.friendTextCtrl.GetValue()
        user=self.userTextCtrl.GetValue()
        msg=self.sendMessageText.GetValue()
        data="mesS desS %s desE souS %s souE conS %s conE mesE\r\n"%(str(friend),str(user),str(msg))
        self.localFactory.protocolInstance.dataSend(data)
        self.sendMessageText.Clear()
        #self.receMessageText.AppendText("\nYou said: %s"%(msg))
        printdebug("you send: %s"%(msg))
#!XRCED:end-block:xrcclientFrame.OnTool_send
        
#!XRCED:begin-block:xrcclientFrame.OnTool_connectTool
    def OnTool_connectTool(self, evt):
        # Replace with event handler code
        printdebug("OnTool_connectTool()")
        self.localFactory=client_twisted.xdClientFactory(str(self.userTextCtrl.GetLabel()),str(self.passwordTextCtrl.GetLabel()))
        self.clientConnector=reactor.connectTCP(str(self.serverTextCtrl.GetLabel()),8002,self.localFactory)
        printdebug("clientConnector start")
        printdebug(self.clientConnector.state)
        printdebug("clientConnector end")
        if self.clientConnector.state=='''connecting''':
            printdebug("connected connected connected connected connected ")
            self.statusText.SetLabel("  Connectted server")

#!XRCED:begin-block:xrcclientFrame.OnTool_loseconnectTool
    def OnTool_loseconnectTool(self, evt):
        # Replace with event handler code
        self.localFactory.protocolInstance.transport.loseConnection()
        printdebug("OnTool_loseconnectTool()")
#!XRCED:end-block:xrcclientFrame.OnTool_loseconnectTool   


#!XRCED:end-block:xrcclientFrame.OnTool_connectTool     

#!XRCED:begin-block:xrcclientFrame.OnTool_closeTool
    def OnTool_closeTool(self, evt):
        # Replace with event handler code
        printdebug("OnTool_closeTool()")
        self.Destroy()
#!XRCED:end-block:xrcclientFrame.OnTool_closeTool        
   
    def refreshReceMessage(self,src,dst,message):
        self.receMessageText.AppendText("\n"+message)    

    def refreshSendMessage(self,src,dst,message):
        self.receMessageText.AppendText("\n"+message)    
        
if __name__ == '__main__':
#    app = wx.PySimpleApp()
#    frame = client(None)
#    frame.Show()
#    app.MainLoop()
    
    #global frame

    app = wx.PySimpleApp()
    client_twisted.frame = client(None)
    client_twisted.frame.Show()
    reactor.registerWxApp(app)
    reactor.run()