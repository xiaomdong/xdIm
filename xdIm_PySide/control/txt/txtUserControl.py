# -*- coding: UTF-8 -*-

from control.userControl import *

import re

class txtUserControl(userControl):
    '''
                    使用txt文件管理用户，txt文件的格式如下:
        [user=lihai;password=welcome1;friends={liming,xd,tt};]
        [user=ling;assword=welcome1;friends={liming,xd,};]
    '''
    def __init__(self,fileName):
        userControl.__init__(self)
        self.fileName=fileName
        self.userPassword={}
        self.userFriends={}
        self.userLoginlist={}
        self.userDataModifiedFlag=False
#        controlDebug("OK : txtUserControl.__init__")
#        controlDebug(self.userFriends)
#        controlDebug(self.userPassword)
#        return userControlErrValue["OK"]
        
    def userDataInit(self):
        '''
                            打开用户配置文件，初始化用户配置数据
        '''
        if self.userDataModifiedFlag:
            controlDebug(u"txtUserControl TIP: txtUserControl.userDataInit 用户数据已经被修改，不能初始化用户数据")
            return userControlErrValue["ControlDataModified"]
        
        #打开文件
        try:
#            self.fileSlot=open(self.fileName,"rwb")
            self.fileSlot=open(self.fileName,"rb") 
        except:
            controlDebug(u"txtUserControl ERR: txtUserControl.userDataInit 打开用户文件失败")
            return userControlErrValue["ERRopenFile"]
        
        #匹配文件行的正则表达式
        patternStr=r'(^\[user=([a-zA-Z0-9]+);password=([a-zA-Z0-9]+);friends={([a-zA-Z0-9,]*)};\])'
        try:
            self.pattern=re.compile(patternStr)
        except:
            controlDebug(u"txtUserControl ERR: txtUserControl.userDataInit 正则表达式错误")    
            return userControlErrValue["ERRcompileRe"]
         
        for line in self.fileSlot:
            controlDebug(line)
            try:
                userdata=self.pattern.search(line).groups()
            except:
                controlDebug(u"txtUserControl TIP: txtUserControl.userDataInit行信息格式不对，正则表达式不匹配")                  
                userdata=""
            controlDebug(userdata)
            controlDebug( len(userdata))          
            if len(userdata)==4:
                controlDebug(userdata[0]+" "+userdata[1]+" "+userdata[2]+" "+userdata[3])
                controlDebug(userdata)
                user=userdata[1]
                password=userdata[2]
                friends=userdata[3]
                self.userPassword[user]=password
                self.userFriends[user]=friends
                 
        
        self.fileSlot.close()
        controlDebug(u"txtUserControl OK : txtUserControl.userDataInit")
        return userControlErrValue["OK"]
    
    def userDataSave(self):
        '''
                            保存用户配置数据到用户配置文件
        '''
        if not self.userDataModifiedFlag:
            controlDebug(u"txtUserControl TIP: txtUserControl.userDataSave 用户数据没有修改，不需要保存")
            return userControlErrValue["ControlDataNoModified"]
        
        try:
            self.fileSlot=open(self.fileName,"wb")
        except:
            controlDebug(u"txtUserControl ERR: txtUserControl.userDataSave 打开用户文件失败")
            return userControlErrValue["ERRopenFile"]
        
        try:
            for user,password in self.userPassword.items():
                line=r'[user='+user+r';password='+password+r';friends={'+self.userFriends[user]+r'};]'+"\n"     
                self.fileSlot.write(line)
        except:
            controlDebug(u"txtUserControl ERR: txtUserControl.userDataSave 写用户文件失败")            
            self.fileSlot.close()
            return userControlErrValue["ERRwriteFile"]
        
        self.fileSlot.close()
        self.userDataModifiedFlag=True
        controlDebug(u"txtUserControl OK : txtUserControl.userDataSave")
        return userControlErrValue["OK"]

    def userDataSaveAs(self,fileName):
        '''
                            保存用户配置数据到指定的用户配置文件
        '''
        try:
            self.fileSlot=open(fileName,"wb")
        except:
            controlDebug(u"txtUserControl ERR: txtUserControl.userDataSaveAs 打开用户文件失败")
            return userControlErrValue["ERRopenFile"]
        
        try:
            for user,password in self.userPassword.items():
                line=r'[user='+user+r';password='+password+r';friends={'+self.userFriends[user]+r'};]'+"\r\n"
                self.fileSlot.write(line)
        except:
            controlDebug(u"txtUserControl ERR: txtUserControl.userDataSaveAs 写用户文件失败")            
            self.fileSlot.close()
            return userControlErrValue["ERRwriteFile"]
        
        self.fileSlot.close()
        controlDebug(u"txtUserControl OK : txtUserControl.userDataSaveAs")
        return userControlErrValue["OK"]
                
        
    def exit(self):
        '''退出用户管理'''
        self.userDataSave()
        controlDebug(u"txtUserControl OK : txtUserControl.exit")
        return userControlErrValue["OK"]
    
    def addUser(self,user,password):
        '''添加用户'''
        if self.userPassword.has_key(user):
            controlDebug(u"txtUserControl TIP: txtUserControl.addUser 用户已使用")
            return userControlErrValue["HaveUser"]
        
        self.userPassword[user]=password
        self.userFriends[user]='admin'
        self.userDataModifiedFlag=True
        controlDebug(u"txtUserControl OK : txtUserControl.addUser")
        return userControlErrValue["OK"]
    
    def deleteUser(self,user):
        '''删除用户'''
        if not self.userPassword.has_key(user):
            controlDebug(u"txtUserControl TIP: txtUserControl.deleteUser 用户不存在")
            return userControlErrValue["NoUser"]
        
        del(self.userPassword[user])
        del(self.userFriends[user])
        self.userDataModifiedFlag=True
        controlDebug(u"txtUserControl OK : txtUserControl.deleteUser")
        return userControlErrValue["OK"]

    
    def checkUser(self,user,password):
        '''核对用户名和密码是否正确'''
        controlDebug(user+" "+password)
        controlDebug(self.userPassword)
        if not self.userPassword.has_key(user):
            controlDebug(u"txtUserControl TIP: txtUserControl.checkUser 用户不存在")
            return userControlErrValue["NoUser"]
        
        if self.userPassword[user]!=password:
            controlDebug(u"txtUserControl TIP: txtUserControl.checkUser 用户和密码不一致 ")
            return userControlErrValue["UserPasswordErr"]
        controlDebug(u"txtUserControl OK : txtUserControl.checkUser")
        return userControlErrValue["OK"]

    
    def modifyUserPassword(self,user,password):
        '''修改用户密码'''
        if not self.userPassword.has_key(user):
            controlDebug(u"txtUserControl TIP: txtUserControl.modifyUserPassword 用户不存在")
            return userControlErrValue["NoUser"]
        
        self.userPassword[user]=password
        self.userDataModifiedFlag=True
        controlDebug(u"txtUserControl OK : txtUserControl.modifyUserPassword ")
        return userControlErrValue["OK"]


    def getUsers(self):
        '''获取用户列表'''
        return self.userFriends
        
    def getUserFriends(self,user):
        '''获取用户好友列表'''
        if not self.userFriends.has_key(user):
            controlDebug(u"txtUserControl ERR: txtUserControl.getUserFriends 用户不存在")
            return userControlErrValue["NoUser"]
        
        controlDebug(u"txtUserControl OK : txtUserControl.getUserFriends")
        controlDebug(self.userFriends[user])
        return self.userFriends[user]
        
  
    def findUser(self,user):
        '''查询用户是否存在'''
        controlDebug(u"txtUserControl txtUserControl.finedUser :"+ user)
        controlDebug(self.userPassword)
        if not self.userPassword.has_key(user):
            controlDebug(u"txtUserControl TIP: txtUserControl.findUser 用户不存在")
            return userControlErrValue["NoUser"]
        
        controlDebug(u"txtUserControl OK : txtUserControl.finedUser")
        return userControlErrValue["HaveUser"]
  
    def findUserFriend(self,user,friend):
        '''查询用户好友是否存在'''
        controlDebug(u"txtUserControl txtUserControl.findUserFriend :"+ user+" "+friend)
        controlDebug(self.userFriends)
        if not self.userFriends.has_key(user):
            controlDebug(u"txtUserControl TIP: txtUserControl.findUserFriend 用户不存在")
            return userControlErrValue["NoUser"]
        
        userFriends=self.userFriends[user]
        friendsList=userFriends.split(',')
        controlDebug(friendsList)
        
        if friend==user:
            controlDebug(u"txtUserControl TIP: txtUserControl.findUserFriend 用户是用户自身的默认好友")
#            return userControlErrValue["OK"]
        elif friendsList.index(friend)==-1:
            controlDebug(u"txtUserControl TIP: txtUserControl.findUserFriend 用户好友不存在")
            return userControlErrValue["NoUserFriend"]
        
        controlDebug(u"txtUserControl OK : txtUserControl.findUserFriend")
        return userControlErrValue["OK"]
        
  
    def addUserFriend(self,user,friend):
        '''添加用户好友'''
        if not self.userPassword.has_key(user):
            controlDebug(u"txtUserControl TIP: txtUserControl.addUserFriend 用户不存在")
            return userControlErrValue["NoUser"]
        
        if not self.userPassword.has_key(friend):
            controlDebug(u"txtUserControl TIP: txtUserControl.addUserFriend 好友用户不能存在")
            return userControlErrValue["NoFriendUser"]
            
           
        userFriends=self.userFriends[user]
        friendsList=userFriends.split(',')

        try :
            friendsList.index(friend)
            controlDebug(u"txtUserControl TIP: txtUserControl.addUserFriend 用户好友已存在")
            return userControlErrValue["NoUserFriend"]
        except ValueError:
            if self.userFriends[user]=="":
                self.userFriends[user]=friend
            else:
                self.userFriends[user]=self.userFriends[user]+","+friend
                      
        self.userDataModifiedFlag=True
        controlDebug(u"txtUserControl OK : txtUserControl.addUserFriend")
        return userControlErrValue["OK"]
  
    def deleteUserFriend(self,user,friend):
        '''删除用户好友'''
        if not self.userFriends.has_key(user):
            controlDebug(u"txtUserControl TIP: txtUserControl.deleteUserFriend 用户不存在")
            return userControlErrValue["NoUser"]
        
        userFriends=self.userFriends[user]
        friendsList=userFriends.split(',')
        
        try:
            friendsList.index(friend)
        except ValueError:    
            controlDebug(u"txtUserControl TIP: txtUserControl.deleteUserFriend 用户好友不存在")
            return userControlErrValue["NoUserFriend"]

        friendsList.remove(friend)

        if len(friendsList):
            self.userFriends[user]=friendsList[0]
            for item in friendsList[1:]:    
#                print item    
                self.userFriends[user]=self.userFriends[user]+","+item
        else:
            self.userFriends[user]=""        
            
        self.userDataModifiedFlag=True
        controlDebug(u"txtUserControl OK : txtUserControl.deleteUserFriend")    
        return userControlErrValue["OK"]         


    
    def login(self,user):
        '''用户登陆'''
        self.userLoginlist[user]=1
    
    def logout(self,user):
        '''用户退出'''
        del self.userLoginlist[user]
    
    def getUserLogin(self,user):
        '''检查用户是否登陆'''
        controlDebug( u'''检查用户是否登陆 ''' + user)
        if self.userLoginlist.has_key(user):
            if self.userLoginlist[user]==1:
                controlDebug( u'''用户已登陆''')
                return 1
            else:
                controlDebug( u'''用户未登陆''')
    
if __name__=="__main__":
    test=txtUserControl("d:\\xxx.txt")
    test.userDataInit()
#    test.findUser("lihai")
    test.addUser('cc', 'apples')
    
#    test.checkUser('xd1', 'apples')
#    test.addUser('cvs13', 'apples')
##    test.addUserFriend("xd1","cvs13")
#    test.addUserFriend("xd1","cvs14")
    test.addUserFriend("xd1","cvs15")
    test.deleteUserFriend("xd1","cvs15")
        
    test.userDataSave()
    test.userDataSaveAs("d:\\ko.txt")
    