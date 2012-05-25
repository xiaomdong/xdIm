# -*- coding: UTF-8 -*-
import MySQLdb
from control.userControl import *

dataBase="xd_database"
userDataTable="userdata"

class sqlUserControl(userControl):
    def __init__(self,host,databaseUser,databasePassword):
        self.host=host
        self.user=databaseUser
        self.password=databasePassword
        self.dataBase=dataBase
        try:
            self.conn=MySQLdb.connect(self.host,self.user,self.password,self.dataBase)
            self.cursor =self.conn.cursor()
            
            controlDebug("OK : sqlUserControl.__init__ 连接数据库成功")
        except:
            controlDebug("ERR: sqlUserControl.__init__ 连接数据库异常")
            del self
            
    def close(self):
        try:
            self.conn.close()
            controlDebug("OK : sqlUserControl.close 关闭数据库成功")
        except:
            controlDebug("ERR: sqlUserControl.close 关闭数据库连接失败")
            del self    
    
#    def createUserDataBase(self):
#        sql="""CREATE DATABASE 'XXXX'"""
#        self.cursor.execute(sql)


    def addUser(self,user,password):
        status = self.findUser(user)
        if status != userControlErrValue["NoUser"]:
            return status

        sql="""insert into %s value('%s','%s','%sfriends')"""%(userDataTable,user,password,user)
        try:
            if(self.cursor.execute(sql)==1L):
                if(self.addUserFriendsTable(user)==userControlErrValue["OK"]):
                    self.conn.commit()
                    controlDebug("OK : sqlUserControl.addUser 添加用户成功")
                    return userControlErrValue["OK"]
                else:
                    self.conn.rollback()
                    controlDebug("ERR: sqlUserControl.addUser 添加用户失败 1")
                    return userControlErrValue["ERR"]
            else:
                controlDebug ("ERR: sqlUserControl.addUser 添加用户失败 2")
                return userControlErrValue["ERR"]
        except:
            controlDebug("ERR: sqlUserControl.addUser sql执行异常")
            return userControlErrValue["ERRsql"]

    def deleteUser(self,user):
        status = self.findUser(user)
        if status != userControlErrValue["HaveUser"]:
            return status

        sql="""delete from %s where name ='%s'"""%(userDataTable,user)
        try:
            if(self.cursor.execute(sql)==1L):
                if(self.deleteUserFriendsTable(user)==userControlErrValue["OK"]):
                    self.conn.commit()
                    controlDebug("OK : sqlUserControl.deleteUser 删除用户成功")
                    return userControlErrValue["OK"]
                else:
                    self.conn.rollback()
                    controlDebug("ERR: sqlUserControl.deleteUser 删除用户失败 1")
                    return userControlErrValue["ERR"]
            else:
                controlDebug("ERR: sqlUserControl.deleteUser  删除用户失败 2")
                return userControlErrValue["ERR"]
        except:
            controlDebug("ERR: sqlUserControl.deleteUser sql执行异常")
            return userControlErrValue["ERRsql"]

            
    def checkUser(self,user,password):
        sql="""select * from %s where name='%s' """ %(userDataTable,user)
        try:
            if(self.cursor.execute(sql)!=1L):
                controlDebug("ERR: sqlUserControl.checkUser 没有找到用户")
                return userControlErrValue["NoUser"]
        except:
            controlDebug("ERR: sqlUserControl.checkUser sql执行异常")
            return userControlErrValue["ERRsql"]
                
        sql="""select * from %s where name='%s' and password='%s'""" %(userDataTable,user,password)
        try:
            if(self.cursor.execute(sql)!=1L):
                controlDebug("ERR: sqlUserControl.checkUser 没有找到用户")
                return userControlErrValue["UserPasswordErr"]
            else:
                controlDebug("OK : sqlUserControl.checkUser 找到用户")
                return userControlErrValue["OK"]
        except:
            controlDebug("ERR: sqlUserControl.checkUser sql执行异常")
            return userControlErrValue["ERRsql"]


    def modifyUserPassword(self,user,password):
        '''修改用户密码'''
        status = self.findUser(user)
        if status != userControlErrValue["HaveUser"]:
            return status
        
        sql="""update %s set password='%s' where name='%s'""" %(userDataTable,password,user)
        print sql
        try:
            if(self.cursor.execute(sql)==1L):
                controlDebug("OK : sqlUserControl.modifyUserPassword 修改用户密码成功")
                self.conn.commit()
                return userControlErrValue["OK"]
            else:
                controlDebug("ERR: sqlUserControl.modifyUserPassword 修改用户密码失败")
                return userControlErrValue["ERR"]
        except:
            controlDebug("ERR: sqlUserControl.modifyUserPassword sql执行异常")
            return userControlErrValue["ERRsql"]
        
    
    def getUserFriends(self,user):
        sql="""select * from %sfriends """ %(user)
        try:
            self.cursor.execute(sql)
            controlDebug("OK : sqlUserControl.getUserFriends 获取了好友列表")
            return self.cursor.fetchall()
        except:
            controlDebug("ERR: sqlUserControl.getUserFriends sql执行异常")
            return userControlErrValue["ERRsql"]

    def findUser(self,user):
        sql="""select * from %s where name='%s' """ %(userDataTable,user)
        try:
            if(self.cursor.execute(sql)==0L):
                controlDebug("TIP: sqlUserControl.findUser 没有找到用户")
                return userControlErrValue["NoUser"]
            else:
                controlDebug("TIP: sqlUserControl.findUser 找到用户")
                return userControlErrValue["HaveUser"]
        except:
            controlDebug("ERR: sqlUserControl.findUser 执行异常")
            return userControlErrValue["ERRsql"]

    def findUserFriend(self,user,userFriend):
#        userFriends=self.getUserFriends(user)
#        if userFriends== -2 :
#            return -1
#        if (userFriend,) in userFriends :
#            print "存在此好友"
#            return 0
#        else:
#            print "无此好友"
#            return -1
        sql="""select * from %sfriends where friend='%s' """ %(user,userFriend)
        print sql
        try:
            if(self.cursor.execute(sql)==0L):
                controlDebug("TIP: sqlUserControl.findUserFriend 没有找到好友")
                return userControlErrValue["NoUserFriend"]
            else:
                controlDebug("TIP: sqlUserControl.findUserFriend 找到好友")
                return userControlErrValue["HaveUserFirend"]
        except:
            controlDebug("ERR: sqlUserControl.findUserFriend sql执行异常")
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


    def addUserFriend(self,user,friend):
        status = self.findUserFriend(user,friend) 
        if status !=userControlErrValue["NoUserFriend"]:
            return status

        sql="""insert into %sfriends value('%s')"""%(user,friend)
        print sql
#        print self.cursor.execute(sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            controlDebug("OK : sqlUserControl.addUserFriend 添加用户好友成功")
            return userControlErrValue["OK"]
        except:
            controlDebug("ERR: sqlUserControl.addUserFriend sql执行异常")
            return userControlErrValue["ERRsql"]

    def deleteUserFriend(self,user,friend):
        status = self.findUserFriend(user,friend) 
        if status !=userControlErrValue["HaveUserFirend"]:
            return status

        sql="""delete from %sfriends where friend ='%s'"""%(user,friend)
#        print self.cursor.execute(sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            controlDebug("OK : sqlUserControl.deleteUserFriend 删除用户好友成功")
            return userControlErrValue["OK"]
        except:
            controlDebug("ERR: sqlUserControl.deleteUserFriend sql执行异常")
            return userControlErrValue["ERRsql"]

    def addUserFriendsTable(self,user):
        sql="""create table %sfriends (friend varchar(45) NOT NULL)"""%(user)
#        print self.cursor.execute(sql)
        try:
            self.cursor.execute(sql)
            controlDebug("OK : sqlUserControl.addUserFriendsTable 添加用户好友数据库表成功")
            return userControlErrValue["OK"]
        except:
            controlDebug("ERR: sqlUserControl.addUserFriendsTable sql执行异常")
            return userControlErrValue["ERRsql"]

    def deleteUserFriendsTable(self,user):
        sql="""drop table %sfriends """%(user)
#        print self.cursor.execute(sql)
        try:
            self.cursor.execute(sql)
            controlDebug("OK : sqlUserControl.deleteUserFriendsTable 删除用户好友数据库表成功")
            return userControlErrValue["OK"]
        except:
            controlDebug("ERR: sqlUserControl.deleteUserFriendsTable sql执行异常")
            return userControlErrValue["ERRsql"]
