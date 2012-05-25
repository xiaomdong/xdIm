# -*- coding: UTF-8 -*-
'''客户端代码'''

from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor, defer
#from twisted.protocols import basic
from sys import stdin
#from twisted.internet import stdio
#import re

from debug import protocolDebug
from protocol.messageControl.messageControl import userLoginReauest,commMessage,parseCommMessage,friendListRequest

#clientUi = None
#由界面层实例来赋值
#需要实两个函数
#refreshReceMessage
#refreshSendMessage
frame = None

def inputText(factory):
    '''inputText'''
    protocolDebug(u":::: " + factory.user + "\r\n")
    protocolDebug(u":::: " + factory.password + "\r\n")
    if 1 :
        text = stdin.readline()
        factory.buildProtocol().transport.write(text)

def debug_required(func):   
    def warp(*args):
        protocolDebug("*****************"+func.__name__+': start')
        func(*args) 
        protocolDebug("*****************"+func.__name__+': end') 
    return warp   
   
   
class classDecorator(type):   
    def __new__(cls, name, bases, dct):   
        for name, value in dct.iteritems():   
            if not name.startswith('_') and callable(value):
                value = debug_required(value)   
            dct[name] = value   
        return type.__new__(cls, name, bases, dct)   
        
class xdClientProtocol(Protocol,object):
#class xdClientProtocol(Protocol):    
    '''客户端Protocol类'''
    __metaclass__ = classDecorator  
    
    def __init__(self):
        '''__init__'''
#        super(xdClientProtocol, self).__init__()
        self.factory = None
        self.inused = None
        self.getFriendsFlag = None
        self.destinationAddress = None
        self.sourceAddress = None
        self.messageContents = None

        
    def connectionMade(self):
        '''连接时调用,发送用户和密码到服务器'''
        self.inused = 0 #连接服务器标志，用户和密码校验通过
        self.getFriendsFlag = 0 #获取用户列表标志
        msg=userLoginReauest(self.factory.user, self.factory.user, self.factory.user, self.factory.password)
        self.transport.write(msg)
        protocolDebug("connectionMade %s"%(msg))

    def messageSend(self, friend,data):
        '''新数据发送,将数据编码合作一个函数里'''
        if data:
            protocolDebug(u"client_twisted send: %s" % (data))
            msg=commMessage(self.factory.user, friend, data)
            self.transport.write(msg)
                            
    def dataReceived(self, data):
        '''数据接收'''
        protocolDebug("client_twisted.dataReceived 1 received: %s" %(data))
        
        #如果连接标志为0，进行登陆校验
        if not self.inused:
            self.loginCheck(data)
            return
        
        if not self.getFriendsFlag:
            self.getFriends(data)
            return
        
        if self.inused == 1 :
            if self.messageCheck(data):
                try:
                    #显示在ui上的最终值
                    receiveData = self.sourceAddress + " said: " + self.messageContents

                    protocolDebug(u"client_twisted.dataReceived 2 receiveData")
                    self.factory.runControlFunction(self.factory.handleReceMessage,
                                                    None,
                                                    self.sourceAddress,
                                                    self.destinationAddress,
                                                    receiveData)
                    #pylint: disable=W0702 
                except:
                    pass 


    def getFriends(self, message):
        '''获取friedns用户列表'''
        friendlist=parseCommMessage(message)
        try:
            protocolDebug(u"client_twisted.getFriends 3 user friends list " + repr(friendlist))
            protocolDebug(friendlist)
            self.factory.runControlFunction(self.factory.handleFriendlist,None,friendlist)
            #pylint: disable=W0702
        except:
            protocolDebug(u"client_twisted.getFriends 4 get user frends list err")    
        
        self.getFriendsFlag = 1       
        self.factory.runControlFunction(self.factory.handleSuccess,None,8002)

        
    def loginCheck(self, message): 
        '''登陆检查''' 
        result=parseCommMessage(message)
        protocolDebug(u"client_twisted.loginCheck result "+str(result))
        if result:
            #用户密码检测成功后，发送用户friendlist请求
            msg=friendListRequest(self.factory.user, self.factory.user)
            self.transport.write(msg)
            self.inused = 1
            protocolDebug(u"client_twisted.loginCheck 1 ok")
        if not result:
            self.inused = 0
            protocolDebug(u"client_twisted.loginCheck 2 err")
    
    def messageCheck(self, message):
        '''消息解析'''
        result=parseCommMessage(message)
        self.destinationAddress = result[1]
        self.sourceAddress = result[0]
        self.messageContents = result[2]

    
#class xdClientFactory(ClientFactory,object):
class xdClientFactory(ClientFactory):    
    '''客户端工厂类'''
    
#    __metaclass__ = classDecorator
    
    user = ""
    password = ""
    protocol = xdClientProtocol
    protocolInstance = None

    def __init__(self, user, password):
        '''初始化'''
#        super(xdClientFactory, self).__init__()
        self.user = user
        self.password = password
        self.handleConnectionLost = None
        self.handleConnectionFailed = None
        self.handleSuccess = None
        self.handleFailure = None
        self.handleLoginUser = None
        self.handleLogoutUser = None
        self.handleReceMessage = None
        self.handleSendMessage = None
        self.handleFriendlist = None
             
    def startedConnecting(self, connector):
        '''开始连接'''
        protocolDebug(u'client_twisted  Started to connect.')

    def buildProtocol(self, addr):
        '''创建Protocol实例'''
        protocolDebug(u'client_twisted Connected.')
        self.protocolInstance = self.protocol()
        self.protocolInstance.factory = self
        return self.protocolInstance

    def clientConnectionLost(self, connector, reason):
        '''断开连接处理函数'''
        protocolDebug(u'client_twisted xdClientFactory.client_twisted Lost connection. Reason:', reason.getErrorMessage())
        self.runControlFunction(self.handleConnectionLost, reason, connector)
        
    def clientConnectionFailed(self, connector, reason):
        '''连接失败处理函数'''
        protocolDebug(u'client_twisted xdClientFactory.Connection failed. Reason:', reason.getErrorMessage())
        self.runControlFunction(self.handleConnectionFailed, reason, connector)
        
    #注册控制函数
    def registerControlFunction(self,
                                _handleConnectionLost,
                                _handleConnectionFailed,
                                _handleSuccess,
                                _handleFailure,
                                _handleLoginUser,
                                _handleLogoutUser,
                                _handleReceMessage,
                                _handleSendMessage,
                                _handleFriendlist
                                ):
        self.handleConnectionLost = _handleConnectionFailed
        self.handleConnectionFailed = _handleConnectionFailed
        self.handleSuccess = _handleSuccess
        self.handleFailure = _handleFailure
        self.handleLoginUser = _handleLoginUser
        self.handleLogoutUser = _handleLogoutUser
        self.handleReceMessage = _handleReceMessage
        self.handleSendMessage = _handleSendMessage
        self.handleFriendlist = _handleFriendlist    
            
    def runControlFunction(self, fun, data=None, *args):
        df = defer.Deferred()
        print "runControl Function start"
        if fun != None:
            df.addCallback(fun, data)
            df.callback(args)
            print args
        print "runControl Function end"

def handleConnectionLost(connector, reason):  
    protocolDebug(u'client_twisted client_twisted handleConnectionLost:', str(connector), reason.getErrorMessage())

    try:        
        if frame.taskBar:
            frame.taskBar.Destroy()
            frame.taskBar = None
        #pylint: disable=W0702     
    except:
        pass        
    #pylint: disable=E1101     
    reactor.disconnectAll()            
#   reactor.stop()
        
        
def handleConnectionFailed(connector, reason):
    protocolDebug(u'client_twisted Connection handleConnectionFailed:', str(connector), reason.getErrorMessage())
    try:
        #pylint: disable=E1101
        reactor.stop()
        #pylint: disable=W0702
    except:
        pass            

def handleFailure(failure, port):
    '''handleFailure'''
    protocolDebug(u"client_twisted handleFailure 1 : connectin from port %i: %s\r\n" % (
          port, failure.getErrorMessage()))
 
 
def handleRemoveUser(connectuser, noUse):
    '''handleRemoveUser'''
    protocolDebug("client_twisted handleRemoveUser")
    noUse = noUse
    try:
        frame.removeUser(connectuser[0])
        #pylint: disable=W0702
    except:
        pass
    
def handleRefreshSendMessage(data, noUse):
    '''handleRefreshSendMessage'''
    protocolDebug("client_twisted handleRefreshSendMessage")
    noUse = noUse
    try:    
        frame.refreshSendMessage(data[0])
        #pylint: disable=W0702
    except:
        pass    
    
def handleAddUsers(connectuser, self):
    '''handleAddUsers'''
    protocolDebug("client_twisted handleAddUsers")
    try:     
        frame.addUsers(connectuser[0], self)
        #pylint: disable=W0702
    except:
        pass
    
def handleRefreshReceMessage(data, noUse):
    '''handleRefreshReceMessage'''
    protocolDebug("client_twisted handleRefreshReceMessage")
    noUse = noUse
    print data
    print noUse
    try:    
        frame.refreshReceMessage(data[0], data[1], data[2])
        #pylint: disable=W0702
    except:
        pass   

def handleFriendlist(friendlist , noUse):
    '''接收到的消息处理'''
    protocolDebug("client_twisted handleFriendlist start")
    
    protocolDebug("noUse: "+str(noUse))
    protocolDebug("friendlist: "+str(friendlist))
    
    frame.setUserFriends(friendlist[0])
    protocolDebug("client_twisted handleFriendlist end")

def handleSuccess(result, port):
    '''注册给客户端协议，在连接成功时调用'''
    protocolDebug( "client_twisted handleSuccess"+str(port))
    frame.updatePanel()
    protocolDebug(result)
    
def handelFailure(failure, port):
    '''注册给客户端协议，在连接失败时调用'''        
    protocolDebug( "client_twisted handelFailure"+str(port))
    protocolDebug(failure.getErrorMessage())
         
    
def runClient(host, port, user, password):
    '''runClient'''
    client = xdClientFactory(user, password)
    #pylint: disable=E1101
    reactor.connectTCP(host, port, client)
    return client
    
def clientMain(host, port, user, password):
    '''clientMain'''
    connecting = runClient(host, port, user, password)
    connecting.registerControlFunction(handleConnectionLost,
                                       handleConnectionFailed,
                                       handleSuccess,
                                       handleFailure,
                                       handleAddUsers,
                                       handleRemoveUser,
                                       handleRefreshReceMessage,
                                       handleRefreshSendMessage,
                                       handleFriendlist)
    return connecting

if __name__ == "__main__":
    host_ = "localhost"
    port_ = 8002
    clientMain(host_, port_, "cvs", "apples")
    #pylint: disable=E1101
    reactor.run()
