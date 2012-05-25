# -*- coding: UTF-8 -*-
'''
Created on 2010-10-13

@author: x00163361
'''
#import os , sys
import locale
#pylint: disable=W0402 
import string
import re
#from config import *

logFlag=0
printdebugFlag = 1
uiDebugFlag = 0
controlDebugFlag =1
protocolFlag = 1


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
    '''界面模块调试打印'''
    if uiDebugFlag == 1:
        printdebug(*args)
        
def controlDebug(*args):
    '''控制模块调试打印'''  
    if controlDebugFlag == 1:
        printdebug(*args)  
    
def protocolDebug(*args):  
    '''协议模块调试打印'''
    if protocolFlag ==  1:
        printdebug(*args)  
        
def printdebug(*args):
    '''
        Debug打印
    '''
    if not printdebugFlag:
        pass
    else:
        try:
            textencoding = getTextCoding()
        #pylint: disable=W0702    
        except:
#            print "unicode err"
            return    
 
        for arg in args:
            if type(arg) == str:
#                print "textencoding:"+textencoding
                print unicode(arg, textencoding)
            else: 
                print arg
                
                
if __name__ == '__main__':
    print getTextCoding
    printdebug("aa")     
    printdebug(u"aa")
#    printdebug(u"aa 你好")
    
    