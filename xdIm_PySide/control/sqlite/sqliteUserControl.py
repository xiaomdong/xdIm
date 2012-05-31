# -*- coding: UTF-8 -*-
import sqlite3

from control.userControl import *

dataBase = ".\\xd_database"
userDataTable = "userdata"

class sqliteUserControl(userControl):
    def __init__(self, dataBase, userDataTable="userdata"):
        self.dataBase = dataBase
        self.userDataTable = userDataTable
        self.tableUserName = "userName"
        self.tablePassword = "password"
        self.tableFriendTable = "friendTable"
        self.tableFriend = "friend"
        self.userPassword = {}
        self.userFriends = {}
        self.userLoginlist = {}
        
        try:
            self.conn = sqlite3.connect(self.dataBase)
            self.cursor = self.conn.cursor()
            controlDebug(u"OK : sqlUserControl.__init__ 连接数据库成功")
        except:
            controlDebug(u"ERR: sqlUserControl.__init__ 连接数据库异常")
            del self

        
    def userDataInit(self):
        
        sql = """select * from %s  ;""" % (self.userDataTable)
        controlDebug("sql=%s" % (sql))
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            controlDebug(result)
            
            for item in result:
                user = item[0]
                password = item[1]
                self.userPassword[user] = password
                self.userFriends[user]=self.getUserFriends(user)
                controlDebug(self.userFriends[user])            
        except:
            controlDebug(u"ERR: sqlUserControl.checkUser sql执行异常")
            return userControlErrValue["ERRsql"]
                
    def close(self):
        try:
            self.conn.close()
            controlDebug(u"OK : sqlUserControl.close 关闭数据库成功")
        except:
            controlDebug(u"ERR: sqlUserControl.close 关闭数据库连接失败")
            del self    
    
    def createUserDataBase(self):
        #创建用户数据库，如果没有的话会默认创建一个
        sql = "CREATE TABLE IF NOT EXISTS %s\
              (%s nvarchar(45) PRIMARY KEY NOT NULL ,\
              %s nvarchar(45) NOT NULL, \
              %s nvarchar(45)NOT NULL) ;\
              " % (self.userDataTable, self.tableUserName, self.tablePassword, self.tableFriendTable)
        controlDebug("sql=%s" % (sql))    
        self.cursor.execute(sql)
        self.conn.commit() 

    def addUser(self, user, password):
        #向用户数据表添加用户
        status = self.findUser(user)
        if status != userControlErrValue["NoUser"]:
            return status

        #添加用户数据
        sql = """insert into %s values('%s','%s','%sfriends') ;""" % (userDataTable, user, password, user)
        controlDebug("sql=%s" % (sql))
        try:
            self.cursor.execute(sql)
        except:
            controlDebug(u"ERR: sqlUserControl.addUser sql执行异常")
            return userControlErrValue["ERRsql"]
            
        #添加用户friendtable    
        if(self.addUserFriendsTable(user) == userControlErrValue["OK"]):
            self.conn.commit()
            controlDebug(u"OK : sqlUserControl.addUser 添加用户成功")
            self.userFriends[user]=password
            return userControlErrValue["OK"]
        else:
            #如果失败，回滚，添加用户失败
            self.conn.rollback()
            controlDebug(u"ERR: sqlUserControl.addUser 添加用户失败 1")
            return userControlErrValue["ERR"]
        

    def deleteUser(self, user):
        status = self.findUser(user)
        if status != userControlErrValue["HaveUser"]:
            return status

        sql = """delete from %s where %s ='%s' ;""" % (self.userDataTable, self.tableUserName, user)
        controlDebug("sql=%s" % (sql))
        try:
            self.cursor.execute(sql)
            if(self.deleteUserFriendsTable(user) == userControlErrValue["OK"]):
                self.conn.commit()
                controlDebug(u"OK : sqlUserControl.deleteUser 删除用户成功")
                return userControlErrValue["OK"]
            else:
                self.conn.rollback()
                controlDebug(u"ERR: sqlUserControl.deleteUser 删除用户失败 1")
                return userControlErrValue["ERR"]
        except:
            controlDebug(u"ERR: sqlUserControl.deleteUser sql执行异常")
            return userControlErrValue["ERRsql"]

            
    def checkUser(self, user, password):
        sql = """select * from %s where %s='%s' ;""" \
             % (self.userDataTable, self.tableUserName, user)
        controlDebug("sql=%s" % (sql))
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if len(result) == 0:
                controlDebug(u"ERR: sqlUserControl.checkUser 没有找到用户")
                return userControlErrValue["NoUser"]
        except:
            controlDebug(u"ERR: sqlUserControl.checkUser sql执行异常")
            return userControlErrValue["ERRsql"]
                
        sql = """select * from %s where %s='%s' and %s='%s' ;""" \
            % (userDataTable, self.tableUserName, user, self.tablePassword, password)
        controlDebug("sql=%s" % (sql))
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if len(result) == 0:
                controlDebug(u"ERR: sqlUserControl.checkUser 没有找到用户")
                return userControlErrValue["UserPasswordErr"]
            else:
                controlDebug(u"OK : sqlUserControl.checkUser 找到用户")
                return userControlErrValue["OK"]
        except:
            controlDebug(u"ERR: sqlUserControl.checkUser sql执行异常")
            return userControlErrValue["ERRsql"]


    def modifyUserPassword(self, user, password):
        '''修改用户密码'''
        status = self.findUser(user)
        if status != userControlErrValue["HaveUser"]:
            return status
        
        sql = """update %s set %s='%s' where %s='%s' ;""" \
              % (self.userDataTable, self.tablePassword, password, self.tableUserName, user)
        controlDebug("sql=%s" % (sql))
        try:
            self.cursor.execute(sql)
            controlDebug(u"OK : sqlUserControl.modifyUserPassword 修改用户密码成功")
            self.conn.commit()
            return userControlErrValue["OK"]
        except:
            controlDebug(u"ERR: sqlUserControl.modifyUserPassword sql执行异常")
            return userControlErrValue["ERRsql"]
        
    def getUsers(self):
        '''获取用户列表'''
        return self.userFriends
        
    def getUserFriends(self, user):
        sql = """select * from %sfriends ;""" % (user)
        controlDebug("sql=%s" % (sql))
        try:
            self.cursor.execute(sql)
            controlDebug(u"OK : sqlUserControl.getUserFriends 获取了好友列表")
            result = self.cursor.fetchall()
            tmpStr = ""
            for friend in result:
                tmpStr += friend[0]+","
            return tmpStr[0:-1]    
        except:
            controlDebug(u"ERR: sqlUserControl.getUserFriends sql执行异常")
            return userControlErrValue["ERRsql"]

    def findUser(self, user):
        sql = """select * from %s where %s='%s' ;""" \
            % (self.userDataTable, self.tableUserName, user)
        controlDebug("sql=%s" % (sql))
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            controlDebug("result=%s " % result)
            if len(result) == 0:
                controlDebug(u"TIP: sqlUserControl.findUser 没有找到用户")
                return userControlErrValue["NoUser"]
            else:
                controlDebug(u"TIP: sqlUserControl.findUser 找到用户")
                return userControlErrValue["HaveUser"]
        except:
            controlDebug(u"ERR: sqlUserControl.findUser 执行异常")
            return userControlErrValue["ERRsql"]

    def findUserFriend(self, user, userFriend):
        sql = """select * from %sfriends where %s='%s' ;""" % (user, self.tableFriend, userFriend)
        controlDebug("sql=%s" % (sql))
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if len(result) == 0:
                controlDebug(u"TIP: sqlUserControl.findUserFriend 没有找到好友")
                return userControlErrValue["NoUserFriend"]
            else:
                controlDebug(u"TIP: sqlUserControl.findUserFriend 找到好友")
#                return userControlErrValue["HaveUserFirend"]
                return userControlErrValue["OK"]
        except:
            controlDebug(u"ERR: sqlUserControl.findUserFriend sql 执行异常")
            return userControlErrValue["ERRsql"]

#    def checkFriend(self,user,friend):
#        sql="""select * from %sfriends where name='%s' """ %(user,friend)
#        try:
#            if(self.cursor.execute(sql)==0L):
#                print "没有找到好友"
#                return 0
#            else:
#                print "找到好友"
#                return -1
#        except:
#            print "sql执行异常"
#            return -2


    def addUserFriend(self, user, friend):
        status = self.findUserFriend(user, friend) 
        if status != userControlErrValue["NoUserFriend"]:
            return status

        sql = """insert into %sfriends values('%s');""" % (user, friend)
        controlDebug("sql=%s" % (sql))
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            controlDebug(u"OK : sqlUserControl.addUserFriend 添加用户好友成功")
            self.userFriends[user]=self.getUserFriends(user)
            return userControlErrValue["OK"]
        except:
            controlDebug(u"ERR: sqlUserControl.addUserFriend sql执行异常")
            return userControlErrValue["ERRsql"]

    def deleteUserFriend(self, user, friend):
        status = self.findUserFriend(user, friend) 
        if status != userControlErrValue["HaveUserFirend"]:
            return status

        sql = """delete from %sfriends where %s ='%s';""" % (user, self.tableFriend, friend)
        controlDebug("sql=%s" % (sql))
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            controlDebug(u"OK : sqlUserControl.deleteUserFriend 删除用户好友成功")
            return userControlErrValue["OK"]
        except:
            controlDebug(u"ERR: sqlUserControl.deleteUserFriend sql执行异常")
            return userControlErrValue["ERRsql"]

    def addUserFriendsTable(self, user):
        #添加用户friend table
        sql = """CREATE TABLE IF NOT EXISTS %sfriends (friend nvarchar(45) NOT NULL);""" % (user)
        controlDebug("sql %s" % (sql))
        try:
            self.cursor.execute(sql)
            controlDebug(u"OK : sqlUserControl.addUserFriendsTable 添加用户好友数据库表成功")
            return userControlErrValue["OK"]
        except:
            controlDebug(u"ERR: sqlUserControl.addUserFriendsTable sql执行异常")
            return userControlErrValue["ERRsql"]


    def deleteUserFriendsTable(self, user):
        sql = """drop table %sfriends ;""" % (user)
        controlDebug("sql=%s" % (sql))
        try:
            self.cursor.execute(sql)
            controlDebug(u"OK : sqlUserControl.deleteUserFriendsTable 删除用户好友数据库表成功")
            return userControlErrValue["OK"]
        except:
            controlDebug(u"ERR: sqlUserControl.deleteUserFriendsTable sql执行异常")
            return userControlErrValue["ERRsql"]
