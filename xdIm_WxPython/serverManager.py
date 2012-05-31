# -*- coding: UTF-8 -*-


from control.txt.txtUserControl import *
from control.xml.xmlUserControl import *
#from control.mysql.sqlUserControl import *

from ui.serverManager.serverManagerUi import *
from config import *
from debug import *
import gettext
import os,sys
import locale
import string
import re

from wx.lib.wordwrap import wordwrap
from twisted.internet import wxreactor
wxreactor.install()

from twisted.internet import reactor, defer
from protocol.server import server_twisted

_ = wx.GetTranslation

def opj(path):
    """Convert paths to the platform-specific separator"""
    st = apply(os.path.join, tuple(path.split('/')))
    # HACK: on Linux, a leading / gets lost...
    if path.startswith('/'):
        st = '/' + st
    return st

class serverManager(serverManagerUi):
    '''服务器端UI类'''
    
    def __init__(self,parent):
        self.locale = None
        
        #设置语言搜索路径为./lang
        wx.Locale.AddCatalogLookupPathPrefix(opj('./lang'))
        serverManagerUi.__init__(self,parent)
        
        self.readConfig("server.cfg") #读取服务器配置文件

        try:
            self.textencoding = getTextCoding()
        except:
            self.textencoding = None    

        uiDebug(self.textencoding)
        
    def readConfig(self,file):
        '''读取服务器端配置文件'''
        self.Config=serverConfig(file)
        self.ControlMedia=self.Config.getControlMedia() 
        self.ControlMediaPath=self.Config.getControlMediaPath()        
        self.language=self.Config.getLanguage()
        self.userControlPanelString=self.ControlMediaPath
        
        #界面多语处理
        if self.language=="Chinese":
            self.updateLanguage(wx.LANGUAGE_CHINESE_SIMPLIFIED)
            self.setString()
            self.languageComboBox.SetSelection(0)
        elif self.language=="English":
            self.updateLanguage(wx.LANGUAGE_ENGLISH)
            self.setString()
            self.languageComboBox.SetSelection(1)
        else:
            self.updateLanguage(wx.LANGUAGE_CHINESE_SIMPLIFIED)
            self.setString()
            self.languageComboBox.SetSelection(0)
        
        #服务器配置
        if self.ControlMedia == mediaValue["txt"]:
            #txt文件保留用户信息
            self.textUserRadioButton.SetValue(True)
            self.mysqlUserButton.Disable()
            self.textUserButton.Enable()
            self.xmlUserButton.Disable()
            self.users=txtUserControl(self.ControlMediaPath)
            
        elif self.ControlMedia == mediaValue["xml"]:
            #xml文件保留用户信息
            self.xmlUserRadioButton.SetValue(True)
            self.mysqlUserButton.Disable()
            self.textUserButton.Disable()
            self.xmlUserButton.Enable()
            self.users=xmlUserControl(self.ControlMediaPath)
            
        elif self.ControlMedia == mediaValue["mysql"]:
            #mysql数据库保留用户信息   
            self.mysqlUserRadioButton.SetValue(True)    
            self.mysqlUserButton.Enable()
            self.textUserButton.Disable()
            self.xmlUserButton.Disable()

        #设置状态栏
        self.mainStatusBar.SetLabel(self.ControlMediaPath)
        try:     
            self.users.userDataInit()
        except:
            self.users=None
            self.mainStatusBar.SetLabel("")
            self.userControlPanelString=""
          
    def updateLanguage(self, lang):
        '''界面语言变化'''
        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale                    
            self.locale=None
        self.locale = wx.Locale(lang)
        print wx.Locale(lang).GetName()
        if self.locale.IsOk():
            self.locale.AddCatalog('serverManager')
        else:
            self.locale = None     


    def OnButton_textUserButton(self, evt):
        '''txt 用户数据库处理'''
        wildcard = "txt (*.txt)|*.txt"
        try:
            Dir=unicode(os.getcwd(), self.textencoding)
        except:
            Dir=os.getcwd()
        
        #这里的style不能选 wx.CHANGE_DIR，更改后，会引起脚本执行目录的变化  
        dlg = wx.FileDialog(
            self, 
            message="Choose a txt file",
            defaultDir=Dir, 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN
            )

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.mainStatusBar.SetLabel(path)    
            self.userControlPanelString=path
        dlg.Destroy()

        self.users=txtUserControl(self.userControlPanelString)
        if self.users.userDataInit()== userControlErrValue["OK"]:
            self.Config.setContrlMedia("txt")  
            self.Config.setControlMediaPath(self.userControlPanelString)
            self.Config.saveServerConfig()
        else:
            uiDebug("serverManager userDataInit error")
                         
        uiDebug("OnButton_textUserButton()")

    def OnButton_mysqlUserButton(self, evt):
        '''mysql 用户数据库处理,暂时没有添加'''
        self.userControlPanelString="mysql"
        uiDebug("serverManager OnButton_mysqlUserButton()")


    def OnButton_xmlUserButton(self, evt):
        '''xml 用户数据库处理'''
        wildcard = "xml (*.xml)|*.xml"

        try:
            Dir=unicode(os.getcwd(), self.textencoding)
        except:
            Dir=os.getcwd()

        dlg = wx.FileDialog(
            self, message="Choose a xml file",
            defaultDir=Dir, 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN
            )
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.mainStatusBar.SetLabel(path)
            self.userControlPanelString=path    
        dlg.Destroy()  
        
        self.users=xmlUserControl(self.userControlPanelString)
        if self.users.userDataInit()== userControlErrValue["OK"]:
            self.Config.setContrlMedia("xml")  
            self.Config.setControlMediaPath(self.userControlPanelString)
            self.Config.saveServerConfig()
        else:
            uiDebug("serverManager userDataInit error")
            
        uiDebug("serverManager OnButton_xmlUserButton()")


    def OnRadiobutton_textUserRadioButton(self, evt):
        '''用户介质选择 text'''
        serverManagerUi.OnRadiobutton_textUserRadioButton(self, evt);
        self.Config.setContrlMedia("txt")
        self.Config.saveServerConfig()        

        self.mysqlUserButton.Disable()
        self.textUserButton.Enable()
        self.xmlUserButton.Disable()
            
    def OnRadiobutton_mysqlUserRadioButton(self, evt):
        '''用户介质选择 mysql'''        
        serverManagerUi.OnRadiobutton_mysqlUserRadioButton(self, evt);
        self.Config.setContrlMedia("mysql")
        self.Config.saveServerConfig(
                                     )
        self.mysqlUserButton.Enable()
        self.textUserButton.Disable()
        self.xmlUserButton.Disable()    
    
    def OnRadiobutton_xmlUserRadioButton(self, evt):
        '''用户介质选择 xml'''        
        serverManagerUi.OnRadiobutton_xmlUserRadioButton(self, evt);        
        self.Config.setContrlMedia("xml")
        self.Config.saveServerConfig()

        self.mysqlUserButton.Disable()
        self.textUserButton.Disable()
        self.xmlUserButton.Enable()  
        
    def OnCombobox_languageComboBox(self, evt):
        '''语言设置'''
        uiDebug(self.languageComboBox.GetValue())
        if (self.languageComboBox.GetValue()=="Chinese" or self.languageComboBox.GetValue()==u"中文"):
            uiDebug(self.languageComboBox.GetValue())
            self.updateLanguage(wx.LANGUAGE_CHINESE_SIMPLIFIED)
            self.setString()
            self.languageComboBox.SetSelection(0)
            self.Config.setLanguage("Chinese")
        else:
            uiDebug(self.languageComboBox.GetValue())
            self.updateLanguage(wx.LANGUAGE_ENGLISH)
            self.setString()
            self.languageComboBox.SetSelection(1)
            self.Config.setLanguage("English")
        uiDebug("serverManager OnCombobox_languageComboBox()")
    
    def setString(self):
        '''界面设置'''
        uiDebug(self.mainNoteBook);
        uiDebug(self.textUserRadioButton);
        self.mainNoteBook.SetPageText(0,_("Server Control"))
        self.serverStartButton.SetLabel(_("Start Server"))
        self.serverStopButton.SetLabel(_("Stop Server"))
        
        self.mainNoteBook.SetPageText(1,_("User Control"))
        self.textUserRadioButton.SetLabel(_("use txt file control user"))
        self.textUserButton.SetLabel(_("Open txt"))
        self.mysqlUserRadioButton.SetLabel(_("use mysql database control user"))
        self.mysqlUserButton.SetLabel(_("Control"))
        self.xmlUserRadioButton.SetLabel(_("use xml file control user"))
        self.xmlUserButton.SetLabel(_("Open xml"))        
        
        self.mainNoteBook.SetPageText(2,_("System Check"))
        self.killUserButton.SetLabel(_("Kill User"))
        self.messageUserButton.SetLabel(_("Message User"))
        self.addUserButton.SetLabel(_("Add user"))
        self.showAllUsersButton.SetLabel(_("Show all users"))
                        
        self.exitMenuItem.SetText(_("Exit")) 
        self.mainMenuBar.SetLabelTop(0,_("File"))

        self.aboutMenuItem.SetText(_("About"))
        self.mainMenuBar.SetLabelTop(1,_("Help"))

        self.languageComboBox.SetString(0,_("Chinese"))
        self.languageComboBox.SetString(1,_("English"))

    def OnNotebook_page_changed_mainNoteBook(self, evt):
        # Replace with event handler code
        page=self.mainNoteBook.GetCurrentPage()

        if page == self.serverControlPanel:
            self.mainStatusBar.SetLabel(self.serverControlPanelString)
            uiDebug("serverManager serverControlPanel")

        if page == self.userControlPanel:
            self.mainStatusBar.SetLabel(self.userControlPanelString)  
            uiDebug("serverManager userControlPanel")

        if page == self.systemCheckPanel:
            self.mainStatusBar.SetLabel(self.systemCheckPanelString)
            uiDebug("serverManager systemCheckPanel")
        
        uiDebug("serverManager OnNotebook_page_changed_mainNoteBook()")
        
    def addUsers(self,value,instance):
        if self.row==self.userGrid.GetNumberRows():
            self.userGrid.AppendRows() 

        self.userGrid.SetCellValue(self.row,self.col,value);
        self.userGrid.SetCellValue(self.row,self.col+1,repr(instance));
        self.userGirdLocation[value]=self.row
        self.row += 1

    def removeUser(self,value):
        
        if self.userGirdLocation.has_key(value):
            for row in range(0,self.row):
                print "row :%d "%(row) + " "+self.userGrid.GetCellValue(row,0)
                if self.userGrid.GetCellValue(row,0)==value:
                    self.userGrid.DeleteRows(row)
                    self.row -= 1
                    return 
                
    def refreshReceMessage(self,message):
        self.userTextCtrl.AppendText("\n"+message)    

    def refreshSendMessage(self,message):
        self.userTextCtrl.AppendText("\n"+message)    
        
#!XRCED:begin-block:xrcserverManagerFrame.OnButton_killUserButton
    def OnButton_killUserButton(self, evt):
        # Replace with event handler code
#        self.refreshLoginUsers("1")
#        self.userTextCtrl.AppendText("\n"+"test")
        for cell in self.userGrid.GetSelectedCells():
            self.connect.killUser(self.userGrid.GetCellValue(cell[0],cell[1]))
            try:
                self.connect.killUser(self.userGrid.GetCellValue(cell[0],cell[1]))
            except:
                pass    
        uiDebug("serverManager OnButton_killUserButton()")
#!XRCED:end-block:xrcserverManagerFrame.OnButton_killUserButton   
            
#!XRCED:begin-block:xrcserverManagerFrame.OnButton_addUserButton
    def OnButton_addUserButton(self, evt):
        # Replace with event handler code
        print "OnButton_addUserButton()"
#!XRCED:end-block:xrcserverManagerFrame.OnButton_addUserButton        

#!XRCED:begin-block:xrcserverManagerFrame.OnButton_showAllUsersButton
    def OnButton_showAllUsersButton(self, evt):
        # Replace with event handler code
        print "OnButton_showAllUsersButton()"
#!XRCED:end-block:xrcserverManagerFrame.OnButton_showAllUsersButton       



#!XRCED:begin-block:xrcserverManagerFrame.OnTogglebutton_serverStartButton
    def OnTogglebutton_serverStartButton(self, evt):
        # Replace with event handler code
        uiDebug( "serverManagerUi OnTogglebutton_serverStartButton()")
        print self.serverStartButton.GetValue()
        
        if self.serverStartButton.GetValue()==False:
            self.serverStartButton.SetValue(True)
            return
        
        self.mainStatusBar.SetLabel("  server is start")
        self.serverControlPanelString="  server is start"
        self.connect=server_twisted.serverMain(8002,self.users)
        self.serverStopButton.SetValue(False)
        
                
#!XRCED:end-block:xrcserverManagerFrame.OnTogglebutton_serverStartButton        

#!XRCED:begin-block:xrcserverManagerFrame.OnTogglebutton_serverStopButton
    def OnTogglebutton_serverStopButton(self, evt):
        # Replace with event handler code
        uiDebug( "serverManagerUi OnTogglebutton_serverStopButton()")
        
        if self.serverStopButton.GetValue()==False:
            self.serverStopButton.SetValue(True)
            return
        
        self.mainStatusBar.SetLabel("  server is stopped")
        self.serverControlPanelString="  server is stopped"
        if self.connect!=None:
            reactor.disconnectAll()
#            reactor.removeAll()
#            reactor.stop()
        self.serverStartButton.SetValue(False)
#!XRCED:end-block:xrcserverManagerFrame.OnTogglebutton_serverStopButton        


#!XRCED:begin-block:xrcserverManagerFrame.OnMenu_exitMenuItem
    def OnMenu_exitMenuItem(self, evt):
        # Replace with event handler code
        uiDebug( "serverManagerUi OnMenu_exitMenuItem()")
        self.Destroy()
#!XRCED:end-block:xrcserverManagerFrame.OnMenu_exitMenuItem        

#!XRCED:begin-block:xrcserverManagerFrame.OnMenu_aboutMenuItem
    def OnMenu_aboutMenuItem(self, evt):
        # Replace with event handler code
        uiDebug( "serverManagerUi OnMenu_aboutMenuItem()")
        info = wx.AboutDialogInfo()
        info.Name = "xdIm"
        info.Version = "0.2.0"
        info.Copyright = "(C) 2008-2010 Programmers and Coders Everywhere"
        info.Description = wordwrap(
            "\n\nxdIm program is a software program \n\n",
            350, wx.ClientDC(self))
        info.WebSite = ("http://www.xdIm.org/", "xdIm home page")
        info.Developers = ["xd"]
        wx.AboutBox(info)
#!XRCED:end-block:xrcserverManagerFrame.OnMenu_aboutMenuItem        
        
          
if __name__ == '__main__':
#    app = wx.PySimpleApp()
#    frame = serverManager(None)
#    frame.Show()
#    app.MainLoop()
    
#    app = MyApp(0)
#    app.MainLoop()

    app = wx.App()
    server_twisted.frame = serverManager(None)
    server_twisted.frame.Show()
    reactor.registerWxApp(app)
    reactor.run()


        