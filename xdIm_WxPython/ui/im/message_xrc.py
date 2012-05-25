# This file was automatically generated by pywxrc.
# -*- coding: UTF-8 -*-

import wx
import wx.xrc as xrc

__res = None

def get_resources():
    """ This function provides access to the XML resources in this module."""
    global __res
    if __res == None:
        __init_resources()
    return __res




class xrcclientFrame(wx.Frame):
#!XRCED:begin-block:xrcclientFrame.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcclientFrame.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PreFrame()
        self.PreCreate(pre)
        get_resources().LoadOnFrame(pre, parent, "clientFrame")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers

        self.Bind(wx.EVT_TOOL, self.OnTool_copyTool, id=xrc.XRCID('copyTool'))
        self.Bind(wx.EVT_TOOL, self.OnTool_pasteTool, id=xrc.XRCID('pasteTool'))
        self.Bind(wx.EVT_TOOL, self.OnTool_sendTool, id=xrc.XRCID('sendTool'))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

#!XRCED:begin-block:xrcclientFrame.OnTool_copyTool
    def OnTool_copyTool(self, evt):
        # Replace with event handler code
        print "OnTool_copyTool()"
#!XRCED:end-block:xrcclientFrame.OnTool_copyTool        

#!XRCED:begin-block:xrcclientFrame.OnTool_pasteTool
    def OnTool_pasteTool(self, evt):
        # Replace with event handler code
        print "OnTool_pasteTool()"
#!XRCED:end-block:xrcclientFrame.OnTool_pasteTool        

#!XRCED:begin-block:xrcclientFrame.OnTool_sendTool
    def OnTool_sendTool(self, evt):
        # Replace with event handler code
        print "OnTool_sendTool()"
#!XRCED:end-block:xrcclientFrame.OnTool_sendTool        

#!XRCED:begin-block:xrcclientFrame.OnClose
    def OnClose(self, evt):
        # Replace with event handler code
        print "OnClose()"
#!XRCED:end-block:xrcclientFrame.OnClose        




# ------------------------ Resource data ----------------------

def __init_resources():
    global __res
    __res = xrc.EmptyXmlResource()

    wx.FileSystem.AddHandler(wx.MemoryFSHandler())

    message_xrc = '''\
<?xml version="1.0" ?><resource>
  <object class="wxFrame" name="clientFrame">
    <object class="wxBoxSizer">
      <orient>wxVERTICAL</orient>
      <object class="sizeritem">
        <object class="wxPanel" name="mainPanel">
          <object class="wxBoxSizer">
            <orient>wxVERTICAL</orient>
            <object class="sizeritem">
              <object class="wxPanel" name="receMesPanel">
                <object class="wxBoxSizer">
                  <orient>wxVERTICAL</orient>
                  <object class="sizeritem">
                    <object class="wxTextCtrl" name="receMessageText">
                      <style>wxTE_MULTILINE</style>
                    </object>
                    <option>-1</option>
                    <flag>wxEXPAND</flag>
                  </object>
                </object>
                <size>250,100</size>
                <bg>#515CAE</bg>
              </object>
              <option>1</option>
              <flag>wxEXPAND</flag>
            </object>
            <object class="sizeritem">
              <object class="wxPanel" name="sendMesPanel">
                <object class="wxBoxSizer">
                  <orient>wxVERTICAL</orient>
                  <object class="sizeritem">
                    <object class="wxToolBar" name="sendMesTool">
                      <object class="tool" name="copyTool">
                        <bitmap stock_id="wxART_COPY"/>
                        <label>copy</label>
                        <XRCED>
                          <events>EVT_TOOL</events>
                        </XRCED>
                      </object>
                      <object class="tool" name="pasteTool">
                        <bitmap stock_id="wxART_PASTE"/>
                        <label>paste</label>
                        <XRCED>
                          <events>EVT_TOOL</events>
                        </XRCED>
                      </object>
                      <object class="tool" name="sendTool">
                        <bitmap stock_id="wxART_QUIT"/>
                        <label>send</label>
                        <XRCED>
                          <events>EVT_TOOL</events>
                        </XRCED>
                      </object>
                      <style>wxTB_FLAT|wxTB_TEXT|wxTB_HORZ_TEXT</style>
                    </object>
                    <option>0</option>
                    <flag>wxEXPAND</flag>
                  </object>
                  <object class="sizeritem">
                    <object class="wxTextCtrl" name="sendMessageText">
                      <style>wxTE_MULTILINE</style>
                    </object>
                    <option>1</option>
                    <flag>wxEXPAND</flag>
                  </object>
                </object>
                <size>250,100</size>
                <bg>#008000</bg>
              </object>
              <option>1</option>
              <flag>wxEXPAND</flag>
            </object>
          </object>
        </object>
        <option>1</option>
        <flag>wxEXPAND</flag>
        <minsize>350,450</minsize>
      </object>
    </object>
    <title>client</title>
    <XRCED>
      <events>EVT_CLOSE</events>
    </XRCED>
  </object>
</resource>'''

    wx.MemoryFSHandler.AddFile('XRC/message/message_xrc', message_xrc)
    __res.Load('memory:XRC/message/message_xrc')


# ----------------------- Gettext strings ---------------------

def __gettext_strings():
    # This is a dummy function that lists all the strings that are used in
    # the XRC file in the _("a string") format to be recognized by GNU
    # gettext utilities (specificaly the xgettext utility) and the
    # mki18n.py script.  For more information see:
    # http://wiki.wxpython.org/index.cgi/Internationalization 
    
    def _(str): pass
    
    _("copy")
    _("paste")
    _("send")
    _("client")

