# -*- coding: UTF-8 -*-
'''
Created on 2010-10-13

@author: x00163361
'''
import os,sys
import locale
import string
import re
#from config import *

userControlebug=1
uIDebug=0
controlDebugtest=0
protocoltest=1

def getTextCoding():
    '''获取unicode编码'''
    textencoding = None
    lang = string.upper(locale.setlocale(locale.LC_ALL, ""))
    if re.match("UTF-8", lang) != None:
        # UTF-8编码
        textencoding = "utf-8"
    elif re.match(r"CHINESE|CP936", lang):
        # Windows下的GB编码
        textencoding = "gb18030"
        #print "windows "+textencoding
    elif re.match(r"GB2312|GBK|GB18030", lang):
        # Linux下的GB编码
        textencoding = "gb18030"
        #print "linux "+textencoding
    else:
        # 其他情况，抛个错误吧
        raise UnicodeError
    return textencoding

def uiDebug(*args):
    if uIDebug==1:
        printdebug(*args)
        
def controlDebug(*args):  
    if controlDebugtest==1:
        printdebug(*args)  
    
def protocolDebug(*args):  
    if protocoltest==1:
        printdebug(*args)  
    
def printdebug(*args):
    '''
        Debug打印
    '''
    if userControlebug==0:
        pass
    else:
        try:
            textencoding=getTextCoding()
        except:
            print "unicode err"
            return    
 
        for arg in args:
            if type(arg)==str:
                print "textencoding:"+textencoding
                print unicode(arg, textencoding)
            else: 
                print arg
                
                
if __name__ == '__main__':
    print getTextCoding
    printdebug("aa")     
    printdebug(u"aa")
    printdebug(u"aa 你好")