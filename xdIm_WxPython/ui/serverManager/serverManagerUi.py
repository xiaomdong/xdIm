# -*- coding: UTF-8 -*-

from serverManager_xrc import * 

from debug import *
import wx.grid

class serverManagerUi(xrcserverManagerFrame):
    def __init__(self,parent):
        xrcserverManagerFrame.__init__(self,parent)
        self.serverManagerFrame = xrc.XRCCTRL(self,"serverManagerFrame")
        self.mainPanel = xrc.XRCCTRL(self,"serverManagerFrame")
        self.mainNoteBook=xrc.XRCCTRL(self,"mainNoteBook")
        
        self.serverControlPanel = xrc.XRCCTRL(self,"serverControlPanel")
        self.languageComboBox = xrc.XRCCTRL(self,"languageComboBox")
        self.serverStartButton = xrc.XRCCTRL(self,"serverStartButton")
        self.serverStopButton = xrc.XRCCTRL(self,"serverStopButton")
        
        self.userControlPanel = xrc.XRCCTRL(self,"userControlPanel")
        self.textUserPanel = xrc.XRCCTRL(self,"textUserPanel")                                
        self.textUserRadioButton = xrc.XRCCTRL(self,"textUserRadioButton")
        self.textUserButton = xrc.XRCCTRL(self,"textUserButton")                
        self.mysqlUserRadioButton = xrc.XRCCTRL(self,"mysqlUserRadioButton")
        self.mysqlUserButton = xrc.XRCCTRL(self,"mysqlUserButton")
        self.xmlUserRadioButton = xrc.XRCCTRL(self,"xmlUserRadioButton")
        self.xmlUserButton = xrc.XRCCTRL(self,"xmlUserButton")                                
        
        
        self.systemCheckPanel = xrc.XRCCTRL(self,"systemCheckPanel")
        uiDebug(repr(self.systemCheckPanel))
        self.userGrid1Panel = xrc.XRCCTRL(self,"userGrid1Panel")
        uiDebug(repr(self.userGrid1Panel))

        #XRCCTRL wx.grid 时需要 import wx.grid
        self.userGrid = xrc.XRCCTRL(self,"userGrid")
        uiDebug("self.userGrid,",repr(self.userGrid))
        self.userGrid.CreateGrid(5,2)
        self.userGridsizer=self.userGrid1Panel.GetSizer()
        self.userGrid1Panel.Update()
                
        self.row=0
        self.col=0
        self.userGirdLocation={}
        self.userGrid.SetColLabelValue(0,"User")
        self.userGrid.SetColLabelValue(1,"Instance")
#        self.userGrid.SetMargins(4,4)
        
        self.userTextCtrl=xrc.XRCCTRL(self,"userTextCtrl")
        
        self.userGrid2Panel = xrc.XRCCTRL(self,"userGrid2Panel")
        self.killUserButton = xrc.XRCCTRL(self,"killUserButton")
        self.messageUserButton = xrc.XRCCTRL(self,"messageUserButton")   
        self.addUserButton = xrc.XRCCTRL(self,"addUserButton")
        self.showAllUsersButton = xrc.XRCCTRL(self,"showAllUsersButton")   

        
#        这样获取MenuBar会有问题        
        self.mainMenuBar1 = xrc.XRCCTRL(self,"mainMenuBar")
#        self.fileMenu = xrc.XRCCTRL(self,"fileMenu")
#        self.exitMenuItem = xrc.XRCCTRL(self,"exitMenuItem")
#        self.helpMenu = xrc.XRCCTRL(self,"helpMenu")
#        self.aboutMenuItem = xrc.XRCCTRL(self,"aboutMenuItem")     

        self.mainMenuBar = self.serverManagerFrame.GetMenuBar()
        self.fileMenu =self.mainMenuBar.GetMenu(0)
        self.exitMenuItem=self.fileMenu.FindItemByPosition(0)
        self.helpMenu =self.mainMenuBar.GetMenu(1)
        self.aboutMenuItem=self.helpMenu.FindItemByPosition(0)
        
        self.mainStatusBar=xrc.XRCCTRL(self,"mainStatusBar")
        self.serverControlPanelString=""
        self.userControlPanelString=""
        self.systemCheckPanelString=""
        self.users=None
        self.connect=None

                    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = serverManagerUi(None)
    frame.Show()
    app.MainLoop()
    
    