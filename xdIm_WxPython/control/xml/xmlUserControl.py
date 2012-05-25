# -*- coding: UTF-8 -*-

from xml.dom import minidom
from control.txt.txtUserControl import *
import re



class xmlUserControl(txtUserControl):
    '''
                    使用xml文件来管理用户数据
                    这里使用userSchema.xsd来定义用户数据结构
        userlist.xml来指定具体的用户数据列表                 
    '''
    
    def __init__(self,fileName):
        txtUserControl.__init__(self,fileName)
        self.userNodes={}
        self.userPasswordNodes={}
        self.userFriendsNodes={}
        self.userLoginlist={}        
        self.userDataModifiedFlag=False
#        controlDebug(u"OK : xmlUserControl.__init__")
        return userControlErrValue["OK"]
    
    def userDataInit(self):
        '''
                            打开用户配置文件，初始化用户配置数据
        '''
        self.xmldoc=minidom.parse(self.fileName)
        userNodes=self.xmldoc.getElementsByTagName('tns:user')
        for Node in userNodes:
            NameNodeList=Node.getElementsByTagName('tns:name')
            userName=NameNodeList[0].childNodes[0].nodeValue
            
            
            userPasswordNode=Node.getElementsByTagName('tns:password')
            password=userPasswordNode[0].childNodes[0].nodeValue
            
            userFriendsNode=Node.getElementsByTagName('tns:friends')
            
            if len(userFriendsNode):
                userFriends=userFriendsNode[0].getElementsByTagName('tns:name')
                friendstr= userFriends[0].childNodes[0].nodeValue
                for friend in userFriends[1:]:
                    friendstr=friendstr+","+friend.childNodes[0].nodeValue
            
            self.userNodes[userName]=Node
            self.userPasswordNodes[userName]=userPasswordNode
            self.userFriendsNodes[userName]=userFriendsNode
            
            self.userPassword[userName]=password
            self.userFriends[userName]=friendstr     
        controlDebug(u"xmlUserControl OK : xmlUserControl.userDataInit")
        return userControlErrValue["OK"]      
    
    def userDataSave(self):
        if not self.userDataModifiedFlag:
            controlDebug(u"xmlUserControl TIP: xmlUserControl.userDataSave 用户数据没有修改，不需要保存")
            return userControlErrValue["ControlDataNoModified"]
        
        try:
            self.fileSlot=open(self.fileName,"w")
        except:
            controlDebug(u"xmlUserControl ERR: xmlUserControl.userDataSave 打开用户文件失败")
            return userControlErrValue["ERRopenFile"]
        self.xmldoc.writexml(self.fileSlot)
        
        self.fileSlot.close()
        self.userDataModifiedFlag=True
        controlDebug(u"xmlUserControl OK : xmlUserControl.userDataSave")
        return userControlErrValue["OK"]
    
    def userDataSaveAs(self,fileName):
        try:
            fileSlot=open(fileName,"w")
        except:
            controlDebug(u"xmlUserControl ERR: xmlUserControl.userDataSave 打开用户文件失败")
            return userControlErrValue["ERRopenFile"]
        
        self.xmldoc.writexml(fileSlot)
        
        fileSlot.close()
        controlDebug(u"xmlUserControl OK : xmlUserControl.userDataSaveAs")
                                           
    
    def exit(self):
        '''退出用户管理'''
        self.userDataSave()
        controlDebug(u"xmlUserControl OK : xmlUserControl.exit")
        return userControlErrValue["OK"]
                            
    def addUser(self,user,password):
        '''添加用户'''
        result=txtUserControl.addUser(self, user,password)
        if result!=userControlErrValue["OK"]:
            return result 
        
        userNode=self.xmldoc.createElement('tns:user')
        
        userNameNode=self.xmldoc.createElement('tns:name')
        userNodeTxt=self.xmldoc.createTextNode(user)
        userNameNode.appendChild(userNodeTxt)
        
        userPasswordNode=self.xmldoc.createElement('tns:password')
        userNodeTxt=self.xmldoc.createTextNode(password)
        userPasswordNode.appendChild(userNodeTxt)

        userFriendsNode=self.xmldoc.createElement('tns:friends')
        userFriendNode=self.xmldoc.createElement('tns:name')
        userFriendTxt=self.xmldoc.createTextNode('admin')
        userFriendNode.appendChild(userFriendTxt)
        userFriendsNode.appendChild(userFriendNode)

        userNode.appendChild(userNameNode)
        userNode.appendChild(userPasswordNode)
        userNode.appendChild(userFriendsNode)
        
        topNode=self.xmldoc.firstChild
        topNode.appendChild(userNode)
        
        self.userNodes[user]=userNode
        self.userPasswordNodes[user]=userPasswordNode
        self.userFriendsNodes[user]=userFriendsNode
        
        self.userPassword[user]=password
        self.userFriends[user]='admin'
        
        self.userDataModifiedFlag=True
        controlDebug(u"xmlUserControl OK : xmlUserControl.addUser")
        return userControlErrValue["OK"]
        
    
    def deleteUser(self,user):
        '''删除用户'''
        result=txtUserControl.deleteUser(self, user)
        if result!=userControlErrValue["OK"]:
            return result  
        
        self.xmldoc.childNodes[0].removeChild(self.userNodes[user])
        
        del(self.userNodes[user])
        del(self.userPasswordNodes[user])
        del(self.userFriendsNodes[user])
                
        self.userDataModifiedFlag=True
        controlDebug(u"xmlUserControl OK : xmlUserControl.deleteUser")
        return userControlErrValue["OK"]

    def modifyUserPassword(self,user,password):
        '''修改用户密码'''
        txtUserControl.modifyUserPassword(self,user,password)
        
        userPasswordNode=self.xmldoc.createElement('tns:password')
        userNodeTxt=self.xmldoc.createTextNode(password)
        userPasswordNode.appendChild(userNodeTxt)
        
        self.userNodes[user].replaceChild(userPasswordNode,self.userPasswordNodes[user][0])

        self.userDataModifiedFlag=True
        controlDebug(u"xmlUserControl OK : xmlUserControl.modifyUserPassword ")
        return userControlErrValue["OK"]
  
    def addUserFriend(self,user,friend):
        '''添加用户好友'''
        result=txtUserControl.addUserFriend(self,user,friend)
        if result!=userControlErrValue["OK"]:
            return result        
        
        userFriendNode=self.xmldoc.createElement('tns:name')
        userFriendTxt=self.xmldoc.createTextNode(friend)
        userFriendNode.appendChild(userFriendTxt)
        
        self.userFriendsNodes[user].appendChild(userFriendNode)
        
        self.userDataModifiedFlag=True
        controlDebug(u"xmlUserControl OK : xmlUserControl.addUserFriend")
        return userControlErrValue["OK"]
  
    def deleteUserFriend(self,user,friend):
        '''删除用户好友'''
        result=txtUserControl.deleteUserFriend(self,user,friend)
        if result!=userControlErrValue["OK"]:
            return result 
        
        friendNodeDic={}
        
        firendNodeList=self.userFriendsNodes[user].getElementsByTagName('tns:name')
        
        for friendNode in firendNodeList:
            friendNodeDic[friendNode.childNodes[0].data]=friendNode
            
        self.userFriendsNodes[user].removeChild(friendNodeDic[friend])
               
        self.userDataModifiedFlag=True
        controlDebug(u"xmlUserControl OK : xmlUserControl.deleteUserFriend")    
        return userControlErrValue["OK"]   
    
    def login(self,user):
        '''用户登陆'''
        self.userLoginlist[user]=1
    
    def logout(self,user):
        '''用户退出'''
        del self.userLoginlist[user]
    
    def getUserLogin(self,user):
        '''检查用户是否登陆'''
        if self.userLoginlist.has_key(user):
            if self.userLoginlist[user]==1:
                return userControlErrValue["OK"]
            
    
if __name__=="__main__":
    test=xmlUserControl("userlist.xml")
    test.userDataInit()
#    test.addUser("kkkk", "password")
#    test.checkUser("kkkk", "password")
#    test.userDataSave()
###    test.deleteUser("kkkk")
###    test.userDataSave()
#    test.modifyUserPassword('xd','apples9')
#    test.userDataSave()
#    test.addUserFriend('xd','kkkk')
#    test.userDataSave()
#    test.deleteUserFriend("xd",'kkkk')
#    test.userDataSave()
    
#    test.deleteUser("kkkk")
#    test.userDataSave()
    test.addUser("cc", "apples")
    test.addUser("mm", "apples")
    test.addUserFriend("cc", "mm")
    test.userDataSaveAs("test.xml")    
##    return 0
#
#    xmldoc=minidom.parse("userlist.xml")
#    userNode=xmldoc.createElement('tns:user')
#    
#    userNameNode=xmldoc.createElement('tns:name')
#    userNameTxt=xmldoc.createTextNode('liming1')
#    userNameNode.appendChild(userNameTxt)
#    
#    userPasswordNode=xmldoc.createElement('tns:password')
#    userPassTxt=xmldoc.createTextNode('apples')
#    userPasswordNode.appendChild(userPassTxt)
#    
#    userFriendNode=xmldoc.createElement('tns:friend')
#    userFriendNode1=xmldoc.createElement('tns:name')
#    userFriendTxt=xmldoc.createTextNode('xd')
#    userFriendNode1.appendChild(userFriendTxt)
#    userFriendNode.appendChild(userFriendNode1)
#    
#    
#    userNode.appendChild(userNameNode)
#    userNode.appendChild(userPasswordNode)
#    userNode.appendChild(userFriendNode)
##    userNode.appendChild(userFriendNode)
#    
##    print userNode.toxml()
##    xmldoc.appendChild(userNode)
#    print xmldoc.toxml()
#    print "***********************"
#    topNode=xmldoc.firstChild
#    topNode.appendChild(userNode)
#    print xmldoc.toxml()
#    f=file('userlist.xml', 'w')
#    xmldoc.writexml(f)
#    f.close()
#    print xmldoc.toxml()
#    topNode=xmldoc.childNodes
#    print xmldoc.childNodes[0]
#    topNode=xmldoc.firstChild
#    print "*************************************************"
#    print topNode.toxml()
#    print "*************************************************"    
#    print topNode.childNodes[0].toxml()
#    print "*************************************************"
#    print topNode.childNodes[1].toxml()
#    print "*************************************************"
#    print topNode.childNodes[2].toxml()    
#    print "*************************************************"
#    print topNode.childNodes[3].toxml()    
#    print "*************************************************"
#    print topNode.childNodes[4].toxml()    
#    print "*************************************************"
#    print topNode.childNodes[5].toxml()    
#    print "*************************************************"
#    print topNode.childNodes[6].toxml()     
#    print "*************************************************"
#    print topNode.lastChild.toxml()
    
#    print xmldoc.childNodes[1].toxml()
    
#    reflist=xmldoc.getElementsByTagName('tns:user')
#    
#    print len(reflist)
#    print reflist[0].toxml()       
#    print reflist[1].toxml()
#    print reflist[2].toxml()
#    bitref = reflist[0]
#    re1=reflist[0].getElementsByTagName('tns:name')
#    print len(re1)
#    print re1[0].toxml()
#    print re1[0].childNodes[0].data
#    re2=reflist[0].getElementsByTagName('tns:password')
#    print re2[0].childNodes[0].data
#    print re1[1].childNodes[0].data
#    print re1[2].childNodes[0].data
#    print "*******************************"
#    print re1[2].childNodes[0].nodeName
#    print re1[2].childNodes[0].nodeValue
#    print "*******************************"
#    print re1[2].nodeValue
#    print re1[0].nodeName 
#    print "*******************************"
#    print re1[0].nodeValue
#    print re1[0].nodeName         
#    print "*******************************"
#    print re1[1].nodeValue
#    print re1[0].nodeName 
#    print reflist[0].childNodes[0].data
#    print reflist[0].childNodes[1].childNodes[0].data
    

#    userlist=reflist.getElementsByTagName('tns:name')
#    print len(userlist)
