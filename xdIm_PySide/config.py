# -*- coding: UTF-8 -*-
'''
Created on 2010-9-19

@author: x00163361
'''

from debug import printdebug
#import os, sys
#import locale
#import string
#import re
import ConfigParser
#from debug import printdebug   
    
mediaValue = {
             "txt"    : "txt"   , #txt
             "MySQL"  : "MySQL" , #mysql
             "Sqlite" : "Sqlite", #sqlite 
             "xml"    : "xml"   , #xml
             }


    
class clientConfig:
    '''
                   客户端配置 
                  用于记录最近登陆的5个用户名，以及服务器地址
    '''
    def __init__(self, configFile):
        self.configFile = configFile
        self.config = ConfigParser.RawConfigParser()
    
class serverConfig:
    '''
                 用于记录服务器端试用的介质控制 txt文件，xml文件，mysql数据库，
                记录默认使用的语言
    '''
    def __init__(self, configFile):
        printdebug(configFile)
        self.configFile = str(configFile)
        self.userControlMedia = ""
        self.userControlMediaPath = ""
        self.language = ""
        self.config = ConfigParser.RawConfigParser()
        self.getServerConfig()
        
        
    def getControlMedia(self):
        '''获取用户存储媒介'''
        printdebug(self.userControlMedia)
        return self.userControlMedia

    def setContrlMedia(self, Media):
        '''设置用户存储媒介'''
        self.userControlMedia = Media
        self.saveServerConfig()
        
    def getControlMediaPath(self):
        '''获取用户存储媒介'''
        printdebug(self.userControlMediaPath)
        return self.userControlMediaPath
    
    def setControlMediaPath(self, userControlMediaPath):
        '''获取用户存储媒介'''
        self.userControlMediaPath = userControlMediaPath
        self.saveServerConfig()
        
    def getLanguage(self):
        '''设置界面语言'''
        printdebug(self.language)
        return self.language
    
    def setLanguage(self, language):
        '''设置界面语言'''
        self.language = language
        self.saveServerConfig()
                
    def getServerConfig(self):
        '''读取服务器配置文件'''
        printdebug(self.configFile)
        data = self.config.read(self.configFile)
        if data:
            #查找配置，填写相应数据    
            try:
                self.userControlMedia = self.config.get('User Control Section', 'media')
                if self.userControlMedia not in mediaValue:
                    self.userControlMedia = 'txt' 
                    self.saveServerConfig()
                self.userControlMediaPath = self.config.get('User Control Section', 'mediaPath')
                self.language = self.config.get('User Control Section', 'language')
                #pylint: disable=W0702     
            except:
                self.saveDefaultConfig()
        else:
            #如果没有找到，填写默认值             
            self.saveDefaultConfig()


    def saveDefaultConfig(self):
        '''保留默认配置'''
        self.config.remove_section('User Control Section')
        self.config.add_section('User Control Section')
        self.config.set('User Control Section', 'language', 'chinese')      #ui语言
        self.config.set('User Control Section', 'media', 'txt')             #媒介类型
        self.config.set('User Control Section', 'mediaPath', 'default.txt') #媒介类型存储路径
        self.userControlMedia = 'txt'
        self.userControlMediaPath = 'default.txt'            
        self.language = 'chinese'
        with open(self.configFile, 'wb') as configfile:
            self.config.write(configfile) 

    def saveServerConfig(self):
        '''保存服务器配置文件'''
        self.config.remove_section('User Control Section')
        self.config.add_section('User Control Section')
        self.config.set('User Control Section', 'language', self.language)
        self.config.set('User Control Section', 'media', self.userControlMedia)
        self.config.set('User Control Section', 'mediaPath', self.userControlMediaPath) 
        with open(self.configFile, 'wb') as configfile:
            self.config.write(configfile) 
         
if __name__ == '__main__':
    useServerConfig = serverConfig("ttt1.cfg")
    useServerConfig.getControlMedia()
    useServerConfig.getControlMediaPath()
    useServerConfig.getLanguage()   
    useServerConfig.setControlMediaPath("mm.txt")
    useServerConfig.saveServerConfig()
#    useServerConfig.setContrlMedia("mysql")
#    print useServerConfig.getControlMedia()
#    useServerConfig.setLanguage("english")
#    print useServerConfig.getLanguage()

