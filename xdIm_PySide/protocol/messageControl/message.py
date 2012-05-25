# -*- coding: utf-8 -*-
'''
Created on 2012-2-7

@author: x00163361
'''
#protoc -I=. --python_out=. .\messageProtocol.proto

import messageProtocol_pb2

class message(object):
    def __init__(self):
        pass
    
    def createFriendMessage(self,com,user,status):
        com.user=user
        com.status=status
    
    def createFriendListMessage(self,com, messageType, *args):
        '''传建friend列表信息'''
        #此处的arg必须是Friend消息
        com.messageFlag = messageType
        for arg in args:
            com.friend.append(arg)
        
    def createUserPasswordMessage(self,com, user, password, messageType, message):
        '''创建用户密码消息'''
        com.user = user
        com.password = password
        com.messageFlag = messageType
        com.message = message

    def createCommunionMessage(self,com, src, dst, messageType, message):
        '''创建消息'''
        com.srcName = src
        com.dstName = dst
        com.messageFlag = messageType
        com.message = message

    def createMessage(self,messageType="communion", *args):
        '''采用工厂模式化，实现类对象的建立'''
        mType = getattr(messageProtocol_pb2, messageType)
        if mType != "":
            comm = mType()
            if messageType == "communion":
                self.createCommunionMessage(comm, args[0], args[1], args[2], args[3])
            if messageType == "userPassword":
                self.createUserPasswordMessage(comm, args[0], args[1], args[2], args[3])
            if messageType == "friendlist":
                self.createFriendListMessage(comm, *args)  
            if messageType == "Friend":
                self.createFriendMessage(comm,args[0],args[1])          
                return comm.SerializeToString()    
        else:
            return None
    
