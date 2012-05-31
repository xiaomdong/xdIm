# -*- coding: UTF-8 -*-
from twisted.internet.protocol import ServerFactory
from twisted.internet import reactor,defer
from twisted.protocols import basic
from sys import stdout
from twisted.internet import stdio
import re
from control.userControl import *

from debug import *

frame=None  
#由界面层实例来赋值
#需要实现四个函数
#refreshReceMessage
#refreshSendMessage
#addUsers
#removeUser


class MyChat(basic.LineReceiver):
    '''一个简单的例子'''
    def connectionMade(self):
        protocolDebug( u"server_twisted Got new client!")
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        protocolDebug( u"server_twisted Lost a client!")
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        protocolDebug( u"server_twisted received", repr(line))
        for c in self.factory.clients:
            c.message(line)

    def message(self, message):
        self.transport.write(message + '\n')

class xdServerProtocol(basic.LineReceiver):
    '''服务器端使用的协议，从LineReceiver继承'''
    inused=0
    loginMessage=""
    connectuser=""
    connectpassword=""
    destinationAddress=""
    sourceAddress=""
    messageContents=""

    def connectionMade(self):
        '''在第一次连接时调用'''
#        protocolDebug("***Get a new client!")
#        self.factory.clients.append(self)
#        self.factory.clientConnect[self.connectuser]=self
#        protocolDebug( self.factory.deferred)
        protocolDebug( u"server_twisted ***xdServerProtocol connectionMade Get a new client! "+self.connectuser)
        
    def connectionLost(self, reason):
        '''在连接断开时调用'''
#        protocolDebug("***Lost a client!\n")
        if self in self.factory.clients:
            self.factory.clients.remove(self)
            if self.factory.clientConnect[self.connectuser] == self:
                #考虑重复登陆的问题
                del self.factory.clientConnect[self.connectuser]
#                frame.removeUser(self.connectuser)
                df=defer.Deferred()
                df.addCallback(handleRemoveUser)
                df.callback(self.connectuser)
                self.factory.user.logout(self.connectuser)
                
            protocolDebug( u"server_twisted connectionLost remove client")
            
#        self.factory.deferred.errback(reason)
        protocolDebug( u"server_twisted ***xdServerProtocol connectionLost Lost a client!"+self.connectuser)
        
    def dataSend(self, data=""):
        '''数据发送'''
        
        #如果消息源地址和目的地址有效，进行消息发送
        protocolDebug( u"server_twisted ***dataSend " + data)
        if self.messageCheck(data)==1:
            if self.factory.clientConnect.has_key(self.destinationAddress):
                if self.factory.clientConnect[self.destinationAddress]!=0:
                    protocolDebug( u"server_twisted ***dataSend data: "+data+"\r\n")
                    self.factory.clientConnect[self.destinationAddress].transport.write(data.encode("utf-8"))
                try:
#                    frame.sendMessageText.AppendText("\n"+data)
#                    frame.refreshSendMessage(data)  
                    df=defer.Deferred()
                    df.addCallback(handleRefreshSendMessage)
                    df.callback(data)
                    
                    protocolDebug( u"server_twisted ***dataSend data: "+data+"\r\n")  
                except:
                    pass
            else:
                protocolDebug( u"server_twisted friend %s is not on line" %self.destinationAddress)     
                
    def messageCheck(self,message):
        '''消息检查，这里没有加密，使用明文传输'''
        patternStr="mesS desS (\S*) desE souS (\S*) souE conS (.*) conE mesE"
        pattern=re.compile(patternStr,re.S)
        try:
            messageGroups=re.search(pattern, message).groups()
        except:
            return 0

        self.destinationAddress=messageGroups[0] #目的连接地址
        self.sourceAddress=messageGroups[1]      #来源地址 
        self.messageContents=messageGroups[2]    #发送消息
        protocolDebug( u"server_twisted message: "+"src: "+self.destinationAddress +", dst: "+self.sourceAddress)  
        
        #察看消息发送的目的地址和来源地址是否有效
        if self.factory.userflag == None:
            if self.factory.user.has_key(self.sourceAddress)==True:
                if self.factory.user.has_key(self.destinationAddress)==True:
                    return 1
        else:
            if self.factory.user.findUser(self.sourceAddress)== userControlErrValue["HaveUser"]:
                if self.factory.user.findUserFriend(self.sourceAddress,self.destinationAddress)== userControlErrValue["OK"]:
                    return 1
                             
    def userCheck(self, usermessage):
        '''The first message form the client is user message ,it include user name and use password'''

        patternStr="userstart (\S*) userend,passwordstart (\S*) passwordend"
        pattern=re.compile(patternStr)
        try:
            user_and_password=re.search(pattern, usermessage).groups()
        except:
            return 0

        self.connectuser=user_and_password[0]     #用户名
        self.connectpassword=user_and_password[1] #密码
        
        if self.factory.userflag ==None:
            if self.factory.user.has_key(self.connectuser)==True:
                pass
            else:
                senddata=u"user name is not right\r\n"
                self.sendLine(senddata.encode("utf-8"))
                self.transport.loseConnection()
                return
            
            if self.factory.user[self.connectuser]==self.connectpassword:
                pass
            else:
                senddata=u"user password is not right\r\n"
                self.sendLine(senddata.encode("utf-8"))
                self.transport.loseConnection()
                return
        else:
            if self.factory.user.checkUser(self.connectuser,self.connectpassword)!= userControlErrValue["OK"]:
                senddata=u"user name or password is not right\r\n"
                self.sendLine(senddata.encode("utf-8"))
                protocolDebug( u"server_twisted ***user name or password is not right\r\n")
                self.transport.loseConnection()
                return
                 
        if self.factory.userflag ==None:                
            self.factory.clients.append(self) #在factory的连接队列中添加连接实例
            self.factory.clientConnect[self.connectuser]=self #保留用户和连接实例的字典
        else:
            if self.factory.user.getUserLogin(self.connectuser)!=1:
#                frame.addUsers(self.connectuser,self)
                df=defer.Deferred()
                df.addCallback(handleAddUsers,self)
                df.callback(self.connectuser)

                self.factory.user.login(self.connectuser)
                self.factory.clients.append(self) #在factory的连接队列中添加连接实例
                self.factory.clientConnect[self.connectuser]=self #保留用户和连接实例的字典
            else:
                self.transport.loseConnection()
                return
                    
        self.inused=1  #client已经登陆
        senddata=u"user and password is right\r\n"
        self.sendLine(senddata.encode("utf-8"))
        protocolDebug( u"server_twisted ***user and password is right")
        
        #发送用户好友列表到客户端
        if self.factory.userflag == None:
            pass
        else:
            protocolDebug( u"server_twisted ***user friends: "+ self.factory.user.getUserFriends(self.connectuser))
#            self.sendLine(self.factory.user.getUserFriends(self.connectuser))
            senddata=u"usersFriendstart %s useFriendsend\r\n"%(self.factory.user.getUserFriends(self.connectuser))
            self.sendLine(senddata.encode("utf-8"))
            protocolDebug( u"server_twisted server_twisted self.sendLine end")
    
    def lineReceived(self, line):
        '''数据接收'''
        '''repr 返回一个对象的字符串体现'''
        #protocolDebug( "xdServerProtocol lineReceived received", repr(line))
        line=line.decode("utf-8")
        try:
#            frame.receMessageText.AppendText("\n"+line)
#            frame.refreshReceMessage(line)
            df=defer.Deferred()
            df.addCallback(handleRefreshReceMessage)
            df.callback(line)
        except:
            pass
        
#        print "received", repr(line)
        
        #如果未登陆，需要进行登陆检测
        if self.inused==0:
            self.userCheck(line)

        #登陆了，开始消息接收
        if self.inused==1:
            if "quit"==line:
                senddata=u"Goodbye."
                self.sendLine(senddata.encode("utf-8"))
                self.transport.loseConnection()
            else:
#                self.sendLine(line.encode("utf-8"))
                self.dataSend(line.encode("utf-8"))
                stdout.write(line+"\r\n")

        protocolDebug( u"server_twisted ***xdServerProtocol lineReceived "+self.connectuser)
                
class xdServerFactory(ServerFactory):
    '''服务器端工厂类，用于生成协议实例'''
    
    protocol = xdServerProtocol             #使用协议 
    clients = []                            #协议实例池
    user ={"xd":"apples","cvs":"apples","a":"a"}    #默认用户字典
    userflag=None                           #user类型标志
    clientConnect={"xd":0,"cvs":0}          #默认客户连接字典
    
    def __init__(self,user=None):
        '''使用user实例代替工厂本省的user字典'''
        self.deferred=defer.Deferred()
        if user!=None:
            self.user=user
            self.userflag=1
            self.clientConnect={}
        protocolDebug( u"server_twisted xdServerFactory init")

    def getConnectUser(self):
        return self.clientConnect.keys()    
        
    def getConnect(self):
        return self.clientConnect
                 
    def startFactory(self):
        pass

    def stopFactory(self):
        pass

    def killUser(self,user):
        protocolDebug( self.clientConnect)
        protocolDebug( u"killUser "+user)
        protocolDebug( self.clientConnect)
        if self.clientConnect.has_key(user):
            protocolDebug( u"killUser loseConnection "+user)
            self.clientConnect[user].transport.loseConnection()
#        self.clients.remove(self.clientConnect[self.connectuser])
#        del self.clientConnect[self.connectuser]

                 
def runServer(port,user):
    protocolDebug( u"server_twisted ****Server is running at port:%d ****\r\n"%(port))
    Server=xdServerFactory(user)
    protocolDebug( user)
    
    reactor.listenTCP(port,Server)
    protocolDebug( u"server_twisted runServer")
    return Server

def handelSuccess(data,port):
    protocolDebug( u"server_twisted handelSuccess start")
    protocolDebug( u"%s"%(data[0]))
    protocolDebug( u"server_twisted Connected from port %i"%(port))
    protocolDebug(  data[1].factory.deferred)
    del data[1].factory.deferred
    data[1].factory.deferred=defer.Deferred();  
    protocolDebug( data[1].factory.deferred)
    data[1].factory.deferred.addCallback(handelSuccess,port)
    protocolDebug( u"server_twisted handelSuccess end")
    #reactor.stop()

def handelFailure(failure,port):
    protocolDebug( u"server_twisted Error: connectin from port %i: %s\r\n"%(
          port,failure.getErrorMessage()))
    #reactor.stop()
 
def handleRemoveUser(connectuser):
    try:
        frame.removeUser(connectuser)
    except:
        pass
    
    
def handleRefreshSendMessage(data):
    try:    
        frame.refreshSendMessage(data)
    except:
        pass    
    
def handleAddUsers(connectuser,self):
    try:     
        frame.addUsers(connectuser,self)
    except:
        pass
def handleRefreshReceMessage(port):
    try:    
        frame.refreshReceMessage(port)
    except:
        pass    
    
def serverMain(port,user):
    connecting=runServer(port,user)
    connecting.deferred.addCallback(handelSuccess,port)
    connecting.deferred.addErrback(handelFailure,port)
    return connecting
    
if __name__ =="__main__":
    '''因为扩展的参数或者关键字参数将会由addCallback或
    addErrback传递给事件处理器，这将会在调用handleSuccess
          和handleFailure时得到端口参数作为第二个参数'''
    port=8001
    connecting=runServer(port,None)
    connecting.addCallback(handelSuccess,port)
    connecting.addErrback(handelFailure,port)
    reactor.run()
