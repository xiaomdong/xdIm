# -*- coding: UTF-8 -*-

#from protocol.client import client_twisted
#from wx.lib.wordwrap import wordwrap

from ui.im.im_xrc import *

#from debug import *

class ImUi(xrcmainFrame):
    def __init__(self, parent):

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


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = ImUi(None)
    frame.Show()
    app.MainLoop()

    

