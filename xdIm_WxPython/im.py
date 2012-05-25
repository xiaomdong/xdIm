# -*- coding: UTF-8 -*-

from twisted.internet import wxreactor
wxreactor.install()
from twisted.internet import reactor, defer
from protocol.client import client_twisted
from wx.lib.wordwrap import wordwrap

from ui.im.imUi import *
from ui.im.loginPanelUi import *
from ui.im.mainPanelUi import *
global clientConnector

from config import *
from debug import *


class ImTaskBarIcon(wx.TaskBarIcon):
    def __init__(self,parent):
        wx.TaskBarIcon.__init__(self)
#        icon = wx.Icon('xrced.ico',wx.BITMAP_TYPE_ICO)
        self.icon = wx.Icon('collman.ico',wx.BITMAP_TYPE_ICO)        
        self.SetIcon(self.icon)

        self.Frame=parent
        wx.EVT_TASKBAR_LEFT_DCLICK(self, self.OnMenuRestore)
        wx.EVT_TASKBAR_RIGHT_DCLICK(self, self.OnMenuExit)
    
    def CreatePopupMenu(self):
        menu1 =  wx.Menu()
        addFriend=menu1.Append(-1,"add new friend")
        config=menu1.Append(-1,"set Config")
        exit=menu1.Append(-1,"Exit")
        print "create popupMenu"
        self.Bind(wx.EVT_MENU, self.OnExit, exit)
        return menu1        
    
    def OnExit(self,evt):
        self.Frame.doClose()
    
    def OnMenuRestore(self,evt):
        #TODONE: 添任务栏的动作
        self.Frame.Hide()
        self.Frame.Show(True)
        self.Frame.CenterOnScreen()
        pass

    def OnMenuExit(self,evt):
        #TODONE: 添任务栏的动作
        pass
#        self.Frame.Hide()
        pass    



class ImFrame(ImUi):
    def __init__(self, parent):
        self.user=""
        self.locale = None
        self.updateLanguage(wx.LANGUAGE_CHINESE_SIMPLIFIED)    
             
        xrcmainFrame.__init__(self, parent)
        self.mainMenuBar = xrc.XRCCTRL(self, "mainMenuBar") 
        self.FileMenu = xrc.XRCCTRL(self, "FileMenu")
        self.loginMenuItem = xrc.XRCCTRL(self, "loginMenuItem")
        self.logoutMenuItem = xrc.XRCCTRL(self, "logoutMenuItem")
        self.operateMenu = xrc.XRCCTRL(self, "operateMenu")
        self.addFriendMenuItem = xrc.XRCCTRL(self, "addFriendMenuItem")
        self.deleteFriendMenuItem = xrc.XRCCTRL(self, "deleteFriendMenuItem")
        self.helpMenu = xrc.XRCCTRL(self, "helpMenu")
        self.aboutMenuItem = xrc.XRCCTRL(self, "aboutMenuItem")

        mainsizer=self.GetSizer() 
        self.mainPanel=loginPanel(self)
        mainsizer.Add(self.mainPanel,1,wx.EXPAND|wx.ADJUST_MINSIZE|wx.FIXED_MINSIZE,0)
        mainsizer.Fit(self)

        try:
            self.textencoding = getTextCoding()
        except:
            self.textencoding = None  
            
        self.connecting=None
        self.friends=[]
        self.taskBar=None

    def __del__(self):
        print "__del__"
        self.taskBar.__del__(self.taskBar)
        self.parent.__del__(self)
                    
    def updatePanel(self):
        uiDebug("im updatePanel() start")
        mainsizer=self.GetSizer() 
        self.mainPanel.Destroy()
        self.mainPanel=mainPanel(self)
        firendItem=self.mainPanel.linkmanTreeCtrl.AddRoot("Friend")
        self.mainPanel.linkmanTreeCtrl.AppendItem(firendItem,self.user)
        uiDebug(self.friends)
        if self.friends!=None:
            for friend in self.friends:
                uiDebug("* "+friend)    
                if friend!="":
                    self.mainPanel.linkmanTreeCtrl.AppendItem(firendItem,friend)
                     
        mainsizer.Add(self.mainPanel,1,wx.EXPAND|wx.ADJUST_MINSIZE|wx.FIXED_MINSIZE,0)
        mainsizer.Fit(self)
        self.taskBar=ImTaskBarIcon(self)
        uiDebug("im updatePanel() end")
     
    def connectServer(self, host, port, user, password, handleSuccess, handelFailure):
        self.user=user
        self.connecting=client_twisted.runClient(host,port,user,password,handleSuccess,handelFailure)
                    
#!XRCED:begin-block:xrcmainFrame.OnMenu_loginMenuItem
    def OnMenu_loginMenuItem(self, evt):
        # Replace with event handler code
#        mainsizer=self.GetSizer() 
##        self.mainPanel.Destroy()
#        self.mainPanel=mainPanel(self)
#        mainsizer.Add(self.mainPanel,1,wx.EXPAND|wx.ADJUST_MINSIZE|wx.FIXED_MINSIZE,0)
#        self.mainPanel.Update()
#        mainsizer.Fit(self)
#        mainsizer.Layout()
#        mainsizer.SetSizeHints(self)
        uiDebug("im OnMenu_loginMenuItem()")
#!XRCED:end-block:xrcmainFrame.OnMenu_loginMenuItem        

#!XRCED:begin-block:xrcmainFrame.OnMenu_logoutMenuItem
    def OnMenu_logoutMenuItem(self, evt):
        # Replace with event handler code
#        self.mainPanel.Destroy()
        uiDebug("im OnMenu_logoutMenuItem()")
#!XRCED:end-block:xrcmainFrame.OnMenu_logoutMenuItem        

#!XRCED:begin-block:xrcmainFrame.OnMenu_addFriendMenuItem
    def OnMenu_addFriendMenuItem(self, evt):
        # Replace with event handler code
        uiDebug("im OnMenu_addFriendMenuItem()")
#!XRCED:end-block:xrcmainFrame.OnMenu_addFriendMenuItem        

#!XRCED:begin-block:xrcmainFrame.OnMenu_deleteFriendMenuItem
    def OnMenu_deleteFriendMenuItem(self, evt):
        # Replace with event handler code
        uiDebug("im OnMenu_deleteFriendMenuItem()")
#!XRCED:end-block:xrcmainFrame.OnMenu_deleteFriendMenuItem        

#!XRCED:begin-block:xrcmainFrame.OnMenu_aboutMenuItem
    def OnMenu_aboutMenuItem(self, evt):
        # Replace with event handler code
        uiDebug("im OnMenu_aboutMenuItem()")
#!XRCED:end-block:xrcmainFrame.OnMenu_aboutMenuItem        

#!XRCED:begin-block:xrcmainFrame.OnClose
    def OnClose(self, evt):

        dlg = wx.MessageDialog(None, "do you want close the Im,if no Im will hide",
                       "A Message Box",
                           wx.YES_NO )
        result=dlg.ShowModal()
        if result == wx.ID_YES:        
            self.locale=True
        else:
            self.locale=False
        
        if self.locale:
            self.doClose()
        else:
            self.Hide()
            
        uiDebug("im OnClose()")
#!XRCED:end-block:xrcmainFrame.OnClose 
    
    def doClose(self):
        if self.taskBar:
            self.taskBar.Destroy()
            self.taskBar=None
        reactor.disconnectAll()    
        reactor.stop()
        

    def updateLanguage(self, lang):
        if lang == wx.LANGUAGE_CHINESE_SIMPLIFIED:
            uiDebug("im updateLanguage chinese")    
            self.locale = wx.Locale(lang)
            self.locale.AddCatalogLookupPathPrefix(r'./lang/zh_CN')
            self.locale.AddCatalog('im')
            
        if lang == wx.LANGUAGE_ENGLISH:
            uiDebug( "im updateLanguage english")
            self.locale = wx.Locale(lang)
            self.locale.AddCatalogLookupPathPrefix(r'./lang/En')
            self.locale.AddCatalog('im')            
            pass  

    def refreshReceMessage(self, src, dst, message):
        if self.mainPanel.messageFrame.has_key(src):
            pass
        else:
            #如果没有窗口，重新创建窗口
            self.mainPanel.createMessageFrame(self.user,src)
            
        try: 
            self.mainPanel.messageFrame[src].receMessageText.AppendText("\n"+message)            
        except:
            uiDebug("im refreshReceMessage error " + src +" " +dst)
            
        
    def refreshSendMessage(self, src, dst, message):
        try:
            self.mainPanel.receMessageText[dst].receMessageText.AppendText("\n"+message)
        except:
            uiDebug("im refreshSendMessage error " + src +" " +dst)
                   
        
    def setUserFriends(self,friends):
        uiDebug("im setUserFriends start")
        self.friends=friends    
        uiDebug("im setUserFriends end")
        
if __name__ == '__main__':
#    app = wx.PySimpleApp()
#    frame = ImFrame(None)
#    frame.Show()
#    app.MainLoop()

    app = wx.PySimpleApp()
    client_twisted.frame = ImFrame(None)
    client_twisted.frame.Show()
    reactor.registerWxApp(app)
    reactor.run()        

