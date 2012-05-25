# -*- coding: UTF-8 -*-
from twisted.internet.protocol import ServerFactory
from twisted.internet import reactor, defer, error
from twisted.protocols import basic
from control.userControl import userControlErrValue


from debug import protocolDebug
from protocol.messageControl.messageControl import userLoginFailed,parseCommMessage,userLoginSucess,friendListresponsion
#from ..messageControl.messageControl import userLoginFailed,parseCommMessage,userLoginSucess,friendlistMessages,friendListresponsion
#from twisted.python import log
#from twisted.python.logfile import DailyLogFile


frame = None  

def debug_required(func):
    def warp(*args):
        protocolDebug("*****************"+func.__name__+': start')
        try:
            protocolDebug("***args:"+str(args))
            return func(*args) 
        finally:
            protocolDebug("*****************"+func.__name__+': end')     
    return warp   
   
   
class classDecorator(type):   
    def __new__(cls, name, bases, dct):   
        for name, value in dct.iteritems():   
            if not name.startswith('_') and callable(value):
                value = debug_required(value)   
            dct[name] = value   
        return type.__new__(cls, name, bases, dct)   
    

class xdServerProtocol(basic.LineReceiver,object):
    '''
           服务器端使用的协议，从LineReceiver继承
    self.factory 由factory 的buildProtocol 动态添加
    '''
    __metaclass__ = classDecorator  
    
    def __init__(self):
        '''__init__'''
        self.factory = None
        self.inused = 0
        self.sendFriendsFlag=0
        self.loginMessage = ""
        self.connectuser = ""
        self.connectpassword = ""
        self.destinationAddress = ""
        self.sourceAddress = ""
        self.messageContents = ""
            
#    def connectionMade(self):
#        '''在第一次连接时调用'''
#        protocolDebug( u"server_twisted.xdServerProtocol.connectionMade 1 Get a new client! ")
        
    #pylint: disable=W0222
    def connectionLost(self, reason):
        '''在连接断开时调用'''
        if self in self.factory.clients:
            self.factory.clients.remove(self)
            if self.factory.clientConnect[self.connectuser] == self:
                #考虑重复登陆的问题
                del self.factory.clientConnect[self.connectuser]
                self.factory.runControlFunction(self.factory.handleLogoutUser, None, self.connectuser)
                if self.factory.userflag != None:
                    self.factory.user.logout(self.connectuser)
            
        
    def dataSend(self, data = ""):
        '''数据发送'''
        #如果消息源地址和目的地址有效，进行消息发送
        result=self.messageCheck(data)
        if result == 1:
            if self.factory.clientConnect.has_key(self.destinationAddress):
                if self.factory.clientConnect[self.destinationAddress]:
                    protocolDebug( u"server_twisted.xdServerProtocol.dataSend 2 data: %s"%data+"\r\n")
                    self.factory.clientConnect[self.destinationAddress].transport.write(data)
                try:
                    self.factory.runControlFunction(self.factory.handleSendMessage, None, data)
                    protocolDebug( u"server_twisted.xdServerProtocol.dataSend 3 data: %s"%data+"\r\n")
                    #pylint: disable=W0702  
                except:
                    pass
                
    def messageCheck(self, message):
        '''消息检查，这里没有加密，使用明文传输'''
        result=parseCommMessage(message)
        self.destinationAddress = result[1] #目的连接地址
        self.sourceAddress = result[0]      #来源地址 
        self.messageContents = result[2]    #发送消息
        
        protocolDebug( u"server_twisted.xdServerProtocol.messageCheck 1 message: " + "src: "+self.destinationAddress +", dst: "+self.sourceAddress)  
        
        #察看消息发送的目的地址和来源地址是否有效
        if self.factory.userflag == None:
            if self.factory.user.has_key(self.sourceAddress):
                if self.factory.user.has_key(self.destinationAddress):
                    return 1 
            return 0    
        else:
            if self.factory.user.findUser(self.sourceAddress) == userControlErrValue["HaveUser"]:
                protocolDebug("HaveUser")
                if self.factory.user.findUserFriend(self.sourceAddress, self.destinationAddress) == userControlErrValue["OK"]:
                    protocolDebug("HaveFriend")
                    return 1
            return 0
                             
    def userCheck(self, usermessage):
        '''The first message form the client is user message ,it include user name and use password'''
        #检查用户登录请求信息 
        result=parseCommMessage(usermessage)
        self.connectuser = result[2]
        self.connectpassword = result[3]
        
        if self.factory.userflag == None:
            if self.factory.user.has_key(self.connectuser):
                pass
            else:
                result=userLoginFailed(self.connectuser,self.connectuser,self.connectuser,self.connectpassword)
                protocolDebug("userCheck 1 user and password is wrong")
                self.transport.write(result)
                self.transport.loseConnection()
                return
            
            if self.factory.user[self.connectuser] == self.connectpassword:
                pass
            else:
                result=userLoginFailed(self.connectuser,self.connectuser,self.connectuser,self.connectpassword)
                protocolDebug("userCheck 2 user and password is wrong")
                self.transport.write(result)
                self.transport.loseConnection()
                return
        else:
            if self.factory.user.checkUser(self.connectuser, self.connectpassword) != userControlErrValue["OK"]:
                result=userLoginFailed(self.connectuser,self.connectuser,self.connectuser,self.connectpassword)
                protocolDebug("userCheck 3 user and password is wrong")
                self.transport.write(result)
                self.transport.loseConnection()
                return
                 
        if self.factory.userflag == None:                
            self.factory.clients.append(self) #在factory的连接队列中添加连接实例
            self.factory.clientConnect[self.connectuser] = self #保留用户和连接实例的字典
        else:
            if self.factory.user.getUserLogin(self.connectuser) != 1:
                self.factory.runControlFunction(self.factory.handleLoginUser, self, self.connectuser)
                self.factory.user.login(self.connectuser)
                self.factory.clients.append(self) #在factory的连接队列中添加连接实例
                self.factory.clientConnect[self.connectuser] = self #保留用户和连接实例的字典
            else:
                self.transport.loseConnection()
                return
                    
        self.inused = 1  #client已经登陆
        result=userLoginSucess(self.connectuser,self.connectuser,self.connectuser,self.connectpassword)
        self.transport.write(result)

        self.factory.runControlFunction(self.factory.handleSuccess, None, self.connectuser)
        
    
    def lineReceived(self, line):
        protocolDebug(line)

    def sendFriends(self):
        #发送用户好友列表到客户端
        senddata=None
        if self.factory.userflag == None:
            protocolDebug( u"server_twisted.xdServerProtocol.userCheck 3 ***user friends: " + "cvs")
            senddata = "cvs"
        else:
            protocolDebug( u"server_twisted.xdServerProtocol.userCheck 4 ***user friends: " + self.factory.user.getUserFriends(self.connectuser))
            senddata = self.factory.user.getUserFriends(self.connectuser).split(",")
        result=friendListresponsion(self.connectuser,self.connectuser,*senddata)
        self.transport.write(result)
        self.sendFriendsFlag=1

                
    def  dataReceived(self, data):
        '''数据接收
        repr 返回一个对象的字符串体现'''
        self.factory.runControlFunction(self.factory.handleReceMessage, None, data)
        try:
            self.factory.runControlFunction(self.factory.handleReceMessage, None, data)
            #pylint: disable=W0702            
        except:
            pass
        
        #如果未登陆，需要进行登陆检测
        if not self.inused:
            self.userCheck(data)
            return
        
        if not self.sendFriendsFlag:
            self.sendFriends()
            return
                    
        #登陆了，开始消息接收
        if self.inused == 1:
            if "quit" == data:
                senddata = u"Goodbye."
                self.dataSend(senddata.encode("utf-8"))
                self.transport.loseConnection()
            else:
                self.dataSend(data)

            
    def rawDataReceived(self, data):
        protocolDebug(data)
                        
#class xdServerFactory(ServerFactory,object):
class xdServerFactory(ServerFactory):    
    '''服务器端工厂类，用于生成协议实例'''
#    __metaclass__ = classDecorator  
    
    protocol = xdServerProtocol             #使用协议 
    clients = []                            #协议实例池
    user = {"xd":"apples", "cvs":"apples", "a":"a"}    #默认用户字典
    userflag = None                           #user类型标志
    clientConnect = {"xd":0, "cvs":0}          #默认客户连接字典
    
    def __init__(self, user = None):
        '''使用user实例代替工厂本省的user字典'''
#        self.deferred=defer.Deferred()
        print user
        if user != None:
            self.user = user
            self.userflag = 1
            self.clientConnect = {}
        protocolDebug( u"server_twisted.xdServerFactory.__init__ init")
        self.handleSuccess     = None
        self.handleFailure     = None
        self.handleLoginUser   = None
        self.handleLogoutUser  = None
        self.handleReceMessage = None
        self.handleSendMessage = None
#        self.registerControlFunction(None, None, None, None, None, None)
    
    def getConnectUser(self):
        return self.clientConnect.keys()    
        
    def getConnect(self):
        return self.clientConnect
                 
    def startFactory(self):
        protocolDebug(u"start Factory")


    def stopFactory(self):
        protocolDebug(u"stop Factory")


    def killUser(self, user):
        '''将用户踢出连接'''
        protocolDebug( u"server_twisted.xdServerFactory.killUser 1")
        if self.clientConnect.has_key(user):
            protocolDebug( u"server_twisted.xdServerFactory.killUser 2 kill user: " + user)
            self.clientConnect[user].transport.loseConnection()
 
        protocolDebug( u"server_twisted.xdServerFactory.killUser 3") 
    
    #注册控制函数
    def registerControlFunction(self, _handleSuccess,
                                _handleFailure,
                                _handleLoginUser,
                                _handleLogoutUser,
                                _handleReceMessage,
                                _handleSendMessage,
                                ):
        self.handleSuccess     = _handleSuccess
        self.handleFailure     = _handleFailure
        self.handleLoginUser   = _handleLoginUser
        self.handleLogoutUser  = _handleLogoutUser
        self.handleReceMessage = _handleReceMessage
        self.handleSendMessage = _handleSendMessage
                
    def runControlFunction(self, fun, data = None, *args):
        df = defer.Deferred()
        if fun != None:
            df.addCallback(fun, data)
            df.callback(args)    
                 
def runServer(port,  user):
    '''runServer'''
    protocolDebug( u"server_twisted.runServer 1 ****Server is running at port:%d ****\r\n"%(port))
    Server = xdServerFactory(user)
    protocolDebug( user)
    
    #pylint: disable=E1101
    reactor.listenTCP(port, Server)
    protocolDebug( u"server_twisted.runServer 2 ")
    return Server

def handleSuccess(data, port):
    '''handleSuccess'''
    data=data
    port=port
    protocolDebug( u"server_twisted.handelSuccess 1 start")
    protocolDebug( u"server_twisted.handelSuccess 2 end")

def handleFailure(failure, port):
    '''handleFailure'''
    protocolDebug( u"server_twisted.handleFailure 1 : connectin from port %i: %s\r\n"%(
          port,failure.getErrorMessage()))
 
 
def handleRemoveUser(connectuser, noUse):
    '''handleRemoveUser'''
    noUse=noUse
    try:
        frame.removeUser(connectuser[0])
        #pylint: disable=W0702
    except:
        pass
    
def handleRefreshSendMessage(data, noUse):
    '''handleRefreshSendMessage'''
    noUse=noUse
    try:    
        frame.refreshSendMessage(data[0])
        #pylint: disable=W0702
    except:
        pass    
    
def handleAddUsers(connectuser, self):
    '''handleAddUsers'''
    try:     
        frame.addUsers(connectuser[0], self)
        #pylint: disable=W0702
    except:
        pass
    
def handleRefreshReceMessage(data, noUse):
    '''handleRefreshReceMessage'''
    noUse=noUse
    try:    
        frame.refreshReceMessage(data[0])
        #pylint: disable=W0702
    except:
        pass    
    
def serverMain(port, user):
    '''serverMain'''
    print user
    connecting = runServer(port, user)
    connecting.registerControlFunction(handleSuccess, 
                                       handleFailure, 
                                       handleAddUsers, 
                                       handleRemoveUser, 
                                       handleRefreshReceMessage, 
                                       handleRefreshSendMessage)
    return connecting
    
if __name__ == "__main__":
    #pylint: disable=W0105
    '''
          因为扩展的参数或者关键字参数将会由addCallback或
    addErrback传递给事件处理器，这将会在调用handleSuccess
          和handleFailure时得到端口参数作为第二个参数
    '''
    
    try:          
        port_ = 8002
        serverMain(port_, None)
        #pylint: disable=E1101
        reactor.run()
    except error.CannotListenError:
        protocolDebug("Can't listen in port %d, maybe some server is running in this port"%(port_))
    
    finally:
        pass

