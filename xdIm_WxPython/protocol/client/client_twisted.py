# -*- coding: UTF-8 -*-
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor,defer
from twisted.protocols import basic
from sys import stdout,stdin
from twisted.internet import stdio
import re

from debug import *

frame=None
#由界面层实例来赋值
#需要实两个函数
#refreshReceMessage
#refreshSendMessage

def inputText(factory):
    protocolDebug( u":::: "+factory.user+"\r\n")
    protocolDebug( u":::: "+factory.password+"\r\n")
    if 1 :
        text=stdin.readline()
        factory.buildProtocol().transport.write(text)

class xdClientProtocol(Protocol):
    '''客户端Protocol类'''
    
    def connectionMade(self):
        '''连接时调用,发送用户和密码到服务器'''
        self.inused=0 #连接服务器标志，用户和密码校验通过
        self.getFriendsFlag=0 #获取用户列表标志
        protocolDebug( u"Debug: "+self.factory.user+" "+self.factory.password+"\r\n")
        sendstr=u"userstart %s userend,passwordstart %s passwordend\r\n"%(self.factory.user,self.factory.password)
        self.transport.write(sendstr.encode("utf-8"))

    def messageSend(self,friend,user,data):
        '''新数据发送,将数据编码合作一个函数里'''
        if data:
            protocolDebug( u"client_twisted send: %s"%(data))
            #按utf-8发送数据，以传递中文，原因twisted不支持部分中文的unicode码
            data=u"mesS desS %s desE souS %s souE conS %s conE mesE\r\n"%(friend,user,data)
            self.transport.write(data.encode("utf-8"))

    def dataSend(self,data):
        '''老数据发送，用于原始ui模型'''
        if data:
            protocolDebug( u"client_twisted send: %s"%(data))
            #按utf-8编码发送数据，以传递中文，原因twisted不支持部分中文的unicode码
            self.transport.write(data.encode("utf-8"))
            try:
                if self.messageCheck(data):
                    try:
                        sendData="you said: "+self.messageContents
                        frame.refreshReceMessage(self.destinationAddress,self.sourceAddress,sendData)
                    except:
                        pass             
            except:
                pass
                            
    def dataReceived(self, data):
        '''数据接收'''
        #按utf-8f方式解码，还原unicode数据
        data=data.decode("utf-8")
        protocolDebug( u"client_twisted received: %s"%(data))
        
        #如果连接标志为0，进行登陆校验
        if not self.inused:
            if not self.loginCheck(data):
                return 
        
        if not self.getFriendsFlag:
            self.getFriends(data)
            
        if self.inused == 1 :
            if self.messageCheck(data):
                try:
                    #显示在ui上的最终值
                    receiveData=self.sourceAddress+" said: "+self.messageContents
                    
                    #生成一个Deffered对象，用于异步处理接收到的数据
                    df=defer.Deferred()
                    df.addCallback(handleMessage,self.destinationAddress,receiveData)
                    df.callback(self.sourceAddress)
                    protocolDebug( u"client_twisted receiveData")
                except:
                    pass 
    

    def getFriends(self,message):
        '''获取friedns用户列表'''
        protocolDebug( u"client_twisted ***getFriends " +message)
        patternStr = "usersFriendstart (.*) useFriendsend"
        pattern=re.compile(patternStr)
        try:
            messageGroups=re.search(pattern, message).groups()
            protocolDebug(messageGroups)
            protocolDebug(messageGroups[0])
        except:
            protocolDebug(u"client_twisted get user frends err")   

        protocolDebug(u"client_twisted ***************")
        protocolDebug(messageGroups[0])
        friendStr="([^,]*)"
        pattern=re.compile(patternStr)
        try:
            friendlist=re.findall(friendStr, messageGroups[0])
            protocolDebug(u"client_twisted user friends list "+repr(friendlist))
            protocolDebug(friendlist)
            protocolDebug(u"client_twisted ----------")
            
            #生成一个Deffered对象，用于异步处理接收到的数据
            df=defer.Deferred()
            df.addCallback(handleFriendlist)
            df.callback(friendlist)
            protocolDebug(u"client_twisted ----------")
        except:
            protocolDebug(u"client_twisted get user frends list err")    
        
        self.getFriendsFlag=1       
        protocolDebug(u"client_twisted ***getFriends")
        self.factory.deferred.callback("client_twisted Connected sucessed")
        
    def loginCheck(self,message): 
        '''登陆检查''' 
        patternStr="user and password is right"
        pattern=re.compile(patternStr)
        try:
            messageGroups=re.search(pattern, message).groups()
            self.inused=1
            protocolDebug(u"client_twisted loginCheck ok")
            return 1
        except:
            self.inused=0
            protocolDebug(u"client_twisted loginCheck err")
            return 0
        
    
    def messageCheck(self,message):
        '''消息解析'''
        patternStr="mesS desS (\S*) desE souS (\S*) souE conS (.*) conE mesE"
        pattern=re.compile(patternStr,re.S)
        try:
            messageGroups=re.search(pattern, message).groups()
        except:
            return 0
        
        self.destinationAddress=messageGroups[0]
        self.sourceAddress=messageGroups[1]
        self.messageContents=messageGroups[2]


class xdClientFactory(ClientFactory):
    '''客户端工厂类'''
    user=""
    password=""
    protocol=xdClientProtocol
    protocolInstance=None

    def __init__(self,user,password):
        self.user=user
        self.password=password
        self.deferred=defer.Deferred()

    def startedConnecting(self, connector):
        protocolDebug( u'client_twisted Started to connect.')

    def buildProtocol(self, addr):
        protocolDebug( u'client_twisted Connected.')
        self.protocolInstance=self.protocol()
        self.protocolInstance.factory=self

        return self.protocolInstance

    def clientConnectionLost(self, connector, reason):
        protocolDebug( u'client_twisted client_twisted Lost connection. Reason:', reason.getErrorMessage())
        try:
            self.deferred.callback(reason)
        except:
            pass    
        
        if frame.taskBar:
            frame.taskBar.Destroy()
            frame.taskBar=None
        reactor.disconnectAll()            
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        protocolDebug( u'client_twisted Connection failed. Reason:', reason.getErrorMessage())
        self.deferred.errback(reason)
        #reactor.stop()
        
        
def handelSuccess(result,port):
    protocolDebug( u"client_twisted OK:Connected from port %i"%port)
    protocolDebug( u"client_twisted message %s"%result)
    if result=="close" :
        reactor.stop()

def handelFailure(failure,port):
    protocolDebug( u"client_twisted Error: connectin from port %i: %s\r\n"%(
          port,failure.getErrorMessage()))
    #reactor.stop()


def handleMessage(source,destin,data):
    '''接收到的消息处理'''
    print "handleMessage: " + source +" " +destin + " " +data
    frame.refreshReceMessage(source,destin,data)

def handleFriendlist(friendlist):
    '''接收到的消息处理'''
    frame.setUserFriends(friendlist)
    
    
def runClient(host,port,user,password,hS=handelSuccess,hF=handelFailure):
    client=xdClientFactory(user,password)
    reactor.connectTCP(host,port,client)
    client.deferred.addCallback(hS,port)
    client.deferred.addErrback(hF,port)
    return client
    
def clientMain(host,port,user,password):
    connecting=runClient(host,port,user,password)
    connecting.addCallback(handelSuccess,port)
    connecting.addErrback(handelFailure,port)
    
if __name__ =="__main__":
    host="localhost"
    port=8001
    connecting=runClient(host,port,"cvs","apples")
#    connecting=runClient(host,port,"cvs","apples1")
#    connecting.addCallback(handelSuccess,port)
#    connecting.addErrback(handelFailure,port)
    reactor.run()

