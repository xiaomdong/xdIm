'''
Created on 2010-12-8

@author: x00163361
'''
from ui.im.mainPanel_xrc import *
from ui.im.messageUi import messageFrame
from config import *
from debug import *


class mainPanel(xrcmainPanel):
    def __init__(self, parent):
        xrcmainPanel.__init__(self, parent)
        self.mainPanel = xrc.XRCCTRL(self, "mainPanel")
        self.mainNotebook = xrc.XRCCTRL(self, "mainNotebook")
        self.linkmanPanel = xrc.XRCCTRL(self, "linkmanPanel")
        self.linkmanTreeCtrl = xrc.XRCCTRL(self, "linkmanTreeCtrl")
#        self.userComboBox = xrc.XRCCTRL(self, "userComboBox")
        self.groupPanel = xrc.XRCCTRL(self, "groupPanel")
#        self.passwordTextCtrl=xrc.XRCCTRL(self, "passwordTextCtrl")
        self.groupTreeCtrl = xrc.XRCCTRL(self, "groupTreeCtrl")
        
        try:
            self.textencoding = getTextCoding()
        except:
            self.textencoding = []  

        self.messageFrame={}
            
#!XRCED:begin-block:xrcmainPanel.OnTree_item_activated_linkmanTreeCtrl
    def OnTree_item_activated_linkmanTreeCtrl(self, evt):
        # Replace with event handler code
        friend= self.linkmanTreeCtrl.GetItemText(self.linkmanTreeCtrl.GetSelection())
        user=self.Parent.user
        if self.messageFrame.has_key(friend):
            print"has "+ friend
            self.messageFrame[friend].Show()
            pass
        else:    
            frame = messageFrame(self,user,friend)
            frame.Show()
            self.messageFrame[friend]=frame
        uiDebug(self)            
        uiDebug("mainPanelUi OnTree_item_activated_linkmanTreeCtrl()")
#!XRCED:end-block:xrcmainPanel.OnTree_item_activated_linkmanTreeCtrl        

    def createMessageFrame(self,user,friend):
        frame = messageFrame(self,user,friend)
#        frame.Show()
        frame.Hide()
        self.messageFrame[friend]=frame
        uiDebug("mainPanelUi createMessageFrame()")
        
#!XRCED:begin-block:xrcmainPanel.OnTree_item_menu_linkmanTreeCtrl
    def OnTree_item_menu_linkmanTreeCtrl(self, evt):
        # Replace with event handler code
        uiDebug("mainPanelUi OnTree_item_menu_linkmanTreeCtrl()")
#!XRCED:end-block:xrcmainPanel.OnTree_item_menu_linkmanTreeCtrl   


