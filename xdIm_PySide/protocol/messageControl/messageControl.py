# -*- coding: utf-8 -*-
'''
Created on 2012-1-20

@author: x00163361
'''
#protoc -I=. --python_out=. .\messageProtocol.proto

import messageProtocol_pb2

def createFriendMessage(com,user,status):
    com.user=user
    com.status=status
    
def createFriendListMessage(com, messageType, *args):
    '''传建friend列表信息'''
    #此处的arg必须是Friend消息
    com.messageFlag = messageType
    for arg in args:
        com.friend.append(arg)
        
def createUserPasswordMessage(com, user, password, messageType, message):
    '''创建用户密码消息'''
    com.user = user
    com.password = password
    com.messageFlag = messageType
    com.message = message

def createCommunionMessage(com, src, dst, messageType, message):
    '''创建消息'''
    com.srcName = src
    com.dstName = dst
    com.messageFlag = messageType
    com.message = message

def createMessage(messageType="communion", *args):
    '''采用工厂模式化，实现类对象的建立'''
    mType = getattr(messageProtocol_pb2, messageType)
    if mType != "":
        comm = mType()
        if messageType == "communion":
            createCommunionMessage(comm, args[0], args[1], args[2], args[3])
        if messageType == "userPassword":
            createUserPasswordMessage(comm, args[0], args[1], args[2], args[3])
        if messageType == "friendList":
            createFriendListMessage(comm, *args)  
        if messageType == "friend":
            createFriendMessage(comm,args[0],args[1])          
        return comm.SerializeToString()    
    else:
        return None
    

def parseMessage(messageType="communion", message=None):
    '''采用工厂模式化，实现类对象的建立'''
    mType = getattr(messageProtocol_pb2, messageType)
    if mType != "":
        comm = mType()
        comm.ParseFromString(message)
        return comm
    else:
        return None
    
    
def userLoginReauest(src, dst, user, password):
    '''client在登录时发送的登录请求，携带用户名和密码'''
    str = createMessage("userPassword", user, password, \
                         messageProtocol_pb2.userPassword.request, \
                         messageProtocol_pb2.userPassword.login)
    return createMessage("communion", src, dst, messageProtocol_pb2.communion.userPassword, str)


def userLoginSucess(src, dst, user, password):
    '''生成用户密码检测成功消息'''
    str = createMessage("userPassword", user, password, \
                         messageProtocol_pb2.userPassword.responsion, \
                         messageProtocol_pb2.userPassword.sucess)
    return createMessage("communion", src, dst, messageProtocol_pb2.communion.userPassword, str)

def userLoginFailed(src, dst, user, password):
    '''生成用户密码检测失败消息''' 
    str = createMessage("userPassword", user, password, \
                         messageProtocol_pb2.userPassword.responsion, \
                         messageProtocol_pb2.userPassword.failed)
    return createMessage("communion", src, dst, messageProtocol_pb2.communion.userPassword, str)

def createFriendOnline(user):
    '''生成用户在线信息'''
    return createMessage("friend", user,messageProtocol_pb2.friend.online)

def createFriendOutline(user):
    '''生成用户离线信息'''
    return createMessage("friend", user,messageProtocol_pb2.friend.outline)

def parseFriend(message):
    if type(message)==unicode:
        message=message.encode("utf-8")
    comm=parseMessage("friend", message)
    if comm!=None:
        if comm.status==messageProtocol_pb2.friend.online:
            return [comm.user,1]
        if comm.status==messageProtocol_pb2.friend.outline:
            return [comm.user,0]

def friendListRequest(src, dst, *args):
    str = createMessage("friendList", messageProtocol_pb2.friendList.request, *args)
    return createMessage("communion", src, dst, messageProtocol_pb2.communion.friendList, str)

def friendListresponsion(src, dst, *args):    
    str = createMessage("friendList", messageProtocol_pb2.friendList.responsion, *args)
    return createMessage("communion", src, dst, messageProtocol_pb2.communion.friendList, str)

def friendListActiveOnline(src, dst, user):
    str=createFriendOnline(user)
    str1 = createMessage("friendList", messageProtocol_pb2.friendList.active, str)
    return createMessage("communion", src, dst, messageProtocol_pb2.communion.friendList, str1)


def friendListActiveOutline(src, dst, user):
    str=createFriendOutline(user)
    str1 = createMessage("friendList", messageProtocol_pb2.friendList.active, str)
    return createMessage("communion", src, dst, messageProtocol_pb2.communion.friendList, str1)
        
def friendlistMessages(src, dst, *args):
    '''生成用户列表消息'''
#    print args
    str = createMessage("friendList", *args)
    return createMessage("communion", src, dst, messageProtocol_pb2.communion.friendList, str)

    
def commMessage(src, dst, message):
    '''生成content消息'''
    return createMessage("communion", src, dst, messageProtocol_pb2.communion.content, message)

def parseCommMessage(message):
    '''解析content消息'''
    if type(message)==unicode:
        message=message.encode("utf-8")
    comm = parseMessage("communion", message)
    if comm != None:
        src = comm.srcName
        dst = comm.dstName
        tmpstr=comm.message
        if type(tmpstr)==unicode:
            tmpstr=tmpstr.encode("utf-8")

        #解析通用消息
        if comm.messageFlag == messageProtocol_pb2.communion.content:
            return [comm.srcName, comm.dstName, comm.message]
        
        #解析登录请求消息
        if comm.messageFlag == messageProtocol_pb2.communion.userPassword:
            mes = parseMessage("userPassword", tmpstr)
            if mes == None:
                return None
            if mes.messageFlag == messageProtocol_pb2.userPassword.responsion:
                if mes.message == messageProtocol_pb2.userPassword.sucess:
                    return True
                if mes.message == messageProtocol_pb2.userPassword.failed:
                    return False
            if mes.messageFlag == messageProtocol_pb2.userPassword.request:
                return [src, dst, mes.user, mes.password]  
        
        #解析用户列表消息
        if comm.messageFlag == messageProtocol_pb2.communion.friendList:
            mes = parseMessage("friendList", comm.message.encode("utf-8"))
            if mes == None:
                return None
            if mes.messageFlag == messageProtocol_pb2.friendList.responsion:
                return mes.friend
            if mes.messageFlag == messageProtocol_pb2.friendList.request:
                return [src, dst]
            if mes.messageFlag == messageProtocol_pb2.friendList.active:
                return mes.friend
    return None    

    
if __name__ == '__main__':
    str = userLoginReauest("xd", "cvs", "xd", "cvs")
    print str
    print len(str)
    str = userLoginSucess("xd", "cvs", "xd", "cvsss")
    print str
    print len(str)
    str = friendlistMessages("xd", "cvs", "xd", "cvs")
    print str
    print len(str)
    

