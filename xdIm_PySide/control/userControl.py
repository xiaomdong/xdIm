# -*- coding: UTF-8 -*-

from debug import *

#err值定义
userControlErrValue={
                     "OK"               : None ,  #成功返回
                     "ControlDataModified"     : 2 ,  #用户数据已经被修改，不能初始化用户数据
                     "ControlDataNoModified"   : 3 ,  #用户数据没有修改，不需要保存
                     "NoUser"           : 4 ,  #用户列表中不存在此用户
                     "HaveUser"         : 5 ,  #用户列表中已使用此用户
                     "UserPasswordErr"  : 6 ,  #用户和密码不一致
                     "NoUserFriend"     : 7 ,  #用户朋友列表中不存在此好友
                     "HaveUserFirend"   : 8 ,  #用户朋友列表中已存在此好友
                     "NoFriendUser"     : 9 ,  #用户列表中不存在此好友用户
                                                      
                     "ERR"              :-1 ,  #失败返回
                     "ERRopenFile"      :-2 ,  #打开用户文件失败
                     "ERRwriteFile"     :-3 ,  #写用户文件失败
                     "ERRcompileRe"     :-4 ,  #正则表达式 compile 错误
                     "ERRsearchRe"      :-5 ,  #正则表达式不匹配
                     "ERRsql"           :-6 ,  #SQL执行异常
                     }

#userControlebug=1
#
#def printdebug(*args):
#    if userControlebug==0:
#        pass
#    else:
#        for arg in args:
#            print arg
        
class userControl():
    '''用户管理基类'''
    
    def __init__(self):
        pass
    
    def addUser(self,user,password):
        '''添加用户'''
        pass
    
    def deleteUser(self,user):
        '''删除用户'''
        pass
    
    def checkUser(self,user,password):
        '''核对用户名和密码是否正确'''
        pass

    def modifyUserPassword(self,user,password):
        '''修改用户密码'''
        pass
    
    def getUsers(self):
        '''获取用户列表'''
        pass
    
    def getUserFriends(self,user):
        '''获取用户好友列表'''
        pass
  
    def findUser(self,user):
        '''查询用户是否存在'''
        pass
  
    def findUserFriend(self,user,friend):
        '''查询用户好友是否存在'''
        pass
  
    def addUserFriend(self,user,friend):
        '''添加用户好友'''
        pass
  
    def deleteUserFriend(self,user,friend):
        '''删除用户好友'''
        pass
    
    def login(self,user):
        '''用户登陆'''
        pass
    
    def logout(self,user):
        '''用户退出'''
        pass
    
    def getUserLogin(self,user):
        '''检查用户是否登陆'''
        pass