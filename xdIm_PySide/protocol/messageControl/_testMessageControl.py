# -*- coding: UTF-8 -*-
'''
Created on 2012-1-29

@author: x00163361
'''
import unittest
from messageControl import *

class messageTest(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass
    def testUserDataInit(self):
        pass
        
    def userLoginMessageTest(self):
        src, dst, user, password="A","B","cvs","apples"
        tempStr1=userLoginReauest(src, dst, user, password)
        com2=parseCommMessage(tempStr1)
        self.assertEqual(com2,[src, dst, user, password],"Err in userLoginReauest")

        tempStr2=userLoginSucess(src, dst, user, password)
        com2=parseCommMessage(tempStr2)
        self.assertEqual(com2,True,"Err in userLoginSucess")
        
        tempStr3=userLoginFailed(src, dst, user, password)
        com3=parseCommMessage(tempStr3)
        self.assertEqual(com3,False,"Err in userLoginFailed")
        
    def friendTest(self):
        user="xd"
        tempStr=createFriendOnline(user)
        users=parseFriend(tempStr)
        self.assertEqual([user,1],users,"Err in createFriendOnline")
        tempStr=createFriendOutline(user)
        users=parseFriend(tempStr)
        self.assertEqual([user,0],users,"Err in createFriendOnline")
            
    def friendlistMessagesTest(self):
        src,dst,f1,f2,f3,f4="A","B","cvs","xd","admin","app"
        tempStr1=friendListRequest(src,dst)
        com2=parseCommMessage(tempStr1)
        self.assertEqual(com2,[src,dst],"OK in friendlistMessages")
        
        tempStr1=friendListresponsion(src,dst,f1,f2,f3,f4)
        com2=parseCommMessage(tempStr1)
        self.assertEqual(com2,[f1,f2,f3,f4],"Err in friendlistMessages")
        
        
        
    def communionMessageTest(self):
        src, dst, message="a","b","hello just a test"
        tempStr1=commMessage(src, dst, message)   
        com2=parseCommMessage(tempStr1)   
        self.assertEqual(com2,[src, dst, message],"Err in commMessage")      
                    
def suite():
    suite_=unittest.TestSuite()
    suite_.addTest(messageTest('userLoginMessageTest'))
    suite_.addTest(messageTest('friendlistMessagesTest'))
    suite_.addTest(messageTest('communionMessageTest'))
    suite_.addTest(messageTest('friendTest'))    
    return suite_

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(suite())
    

