from twisted.internet import wxreactor
wxreactor.install()
from twisted.internet import reactor, defer

from ui.server.server_xrc import *
from protocol.server import server_twisted
from debug import *

class server(xrcserverFrame):
    def __init__(self,parent):
        xrcserverFrame.__init__(self,parent)
        self.serverFrame=xrc.XRCCTRL(self,"serverFrame")
        self.mainPanel=xrc.XRCCTRL(self,"mainPanel")
        self.recMesPanel=xrc.XRCCTRL(self.mainPanel,"receMesPanel")
        self.receMessageText=xrc.XRCCTRL(self.recMesPanel,"receMessageText")

        self.senMesPanel=xrc.XRCCTRL(self.mainPanel,"sendMesPanel")
        self.sendMesTool=xrc.XRCCTRL(self.senMesPanel,"sendMesTool")
        self.copy=xrc.XRCCTRL(self.sendMesTool,"copyTool")
        self.paste=xrc.XRCCTRL(self.sendMesTool,"pasteTool")
        self.send=xrc.XRCCTRL(self.sendMesTool,"sendTool")
        self.sendMessageText=xrc.XRCCTRL(self.senMesPanel,"sendMessageText")

        self.mainToolBar=xrc.XRCCTRL(self,"mainToolBar")
        self.start=xrc.XRCCTRL(self.mainToolBar,"startTool")
        self.stopt=xrc.XRCCTRL(self.mainToolBar,"stoptTool")
        self.close=xrc.XRCCTRL(self.mainToolBar,"closetTool")
        self.statusText=xrc.XRCCTRL(self.mainToolBar,"statusText")

#        self.Bind(wx.EVT_TOOL, self.OnTool_copyTool, id=xrc.XRCID('copyTool'))
#        self.Bind(wx.EVT_TOOL, self.OnTool_pasteTool, id=xrc.XRCID('pasteTool'))
#        self.Bind(wx.EVT_TOOL, self.OnTool_sendTool, id=xrc.XRCID('sendTool'))
#        self.Bind(wx.EVT_KEY_DOWN, self.OnKey_down_sendMessageText, id=xrc.XRCID('sendMessageText'))
#        self.Bind(wx.EVT_TOOL, self.OnTool_startTool, id=xrc.XRCID('startTool'))
#        self.Bind(wx.EVT_TOOL, self.OnTool_stopTool, id=xrc.XRCID('stopTool'))
#        self.Bind(wx.EVT_TOOL, self.OnTool_closeTool, id=xrc.XRCID('closeTool'))
        
#!XRCED:begin-block:xrcserverFrame.OnTool_start
    def OnTool_startTool(self, evt):
        # Replace with event handler code
        uiDebug("123123OnTool_start()")
        self.statusText.SetLabel("  server is start")
        server_twisted.serverMain(8001,None)
#        reactor.listenTCP(8001,xdServerFactory())
#!XRCED:end-block:xrcserverFrame.OnTool_start

#!XRCED:begin-block:xrcserverFrame.OnTool_stop
    def OnTool_stopTool(self, evt):
        # Replace with event handler code
        uiDebug("OnTool_stop()")
        reactor.stop()
        
#!XRCED:end-block:xrcserverFrame.OnTool_stop

    def OnTool_closeTool(self, evt):
        # Replace with event handler code
        uiDebug("OnTool_closeTool()")
        self.Destroy()    

    def refreshReceMessage(self,message):
        self.receMessageText.AppendText("\n"+message)    

    def refreshSendMessage(self,message):
        self.sendMessageText.AppendText("\n"+message) 
        
if __name__ == '__main__':
#    app = wx.PySimpleApp()
#    frame = server(None)
#    frame.Show()
#    app.MainLoop()
    
    #global frame

    app = wx.PySimpleApp()
    server_twisted.frame = server(None)
    server_twisted.frame.Show()
    reactor.registerWxApp(app)
    reactor.run()

