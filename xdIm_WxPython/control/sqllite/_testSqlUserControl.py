# -*- coding: UTF-8 -*-

from sqlUserControl import *
import unittest

class testTxtUserControlTestCase(unittest.TestCase):
    def setUp(self):
        self.userControl1=sqlUserControl("xiaodong","xd","apples")
#        self.userControl1.userDataInit()
#        self.saveUserFriends=self.userControl1.userFriends
#        self.saveUserPassword=self.userControl1.userPassword
        
    def tearDown(self):
#        self.userControl1.userFriends=self.saveUserFriends
#        self.userControl1.userPassword=self.saveUserPassword
        self.userControl1.close()
#        pass
    
    def testUserDataInit(self):
#        self.userControl1.userDataSave()
#        result=self.userControl1.userDataInit()
#        self.assertEqual(result,userControlErrValue["OK"],"Error in userDataInit")
        pass
    
    def testAddDeleteuser(self):
        if self.userControl1.findUser("cc")!=userControlErrValue["HaveUser"]:
            pass
        else:
            print "2222"
            result=self.userControl1.deleteUser("cc")
            self.assertEqual(result,userControlErrValue["OK"],"OK in deleteUser")
        
        print "3333"                 
        result=self.userControl1.addUser("cc", "apples")
        self.assertEqual(result,userControlErrValue["OK"],"OK in addUser")
        result=self.userControl1.deleteUser("cc")
        self.assertEqual(result,userControlErrValue["OK"],"OK in deleteUser")
    
    def testAddDeleteUserFriend(self):
        if self.userControl1.findUser("kk")!=userControlErrValue["HaveUser"]:
            pass
        else:
            self.userControl1.deleteUser("kk")
        
        if self.userControl1.findUser("jj")!=userControlErrValue["HaveUser"]:
            pass
        else:
            self.userControl1.deleteUser("jj")
            
        self.userControl1.addUser("kk", "apples")
        self.userControl1.addUser("jj", "apples")
            
        result=self.userControl1.addUserFriend("kk", "jj")
        self.assertEqual(result,userControlErrValue["OK"],"OK in addUserFriend")
        result=self.userControl1.deleteUserFriend("kk", "jj")
        self.assertEqual(result,userControlErrValue["OK"],"OK in deleteUserFriend")
        
        self.userControl1.deleteUser("kk")
        self.userControl1.deleteUser("jj")

#    def testcheckUserFriend(self):
#        result=self.userControl1.findUserFriend("cc", "mm")
#        self.assertEqual(result,userControlErrValue["NoUserFriend"],"OK in findUserFriend")
            
    def testcheckUser(self):
        self.userControl1.addUser("cc", "apples")
        
        result=self.userControl1.checkUser("cc", "apples")
        self.assertEqual(result,userControlErrValue["OK"],"OK in checkUser")
        
        result=self.userControl1.modifyUserPassword("cc", "6666")
        self.assertEqual(result,userControlErrValue["OK"],"Modified in checkUser")
        
        result=self.userControl1.checkUser("cc", "apples")
        self.assertEqual(result,userControlErrValue["UserPasswordErr"],"UserPasswordErr in checkUser")
        
        self.userControl1.deleteUser("cc")
        
        result=self.userControl1.checkUser("cc", "apples")
        self.assertEqual(result,userControlErrValue["NoUser"],"NoUser in checkUser")
    
    def testUserDataSave(self):
        pass
#        self.userControl1.addUser("cc", "apples")
#        self.userControl1.addUser("mm", "apples")
#        self.userControl1.addUserFriend("cc", "mm")
#        result=self.userControl1.userDataSave()
#        self.assertNotEqual(result,userControlErrValue["ERRopenFile"],"ERRopenFile in userDataInit")        
#        self.assertNotEqual(result,userControlErrValue["ERRwriteFile"],"ERRwriteFile in userDataInit")
#        self.userControl1.deleteUser("cc")
#        self.userControl1.deleteUser("mm")
#        self.assertNotEqual(result,userControlErrValue["ERRopenFile"],"ERRopenFile in userDataInit")        
#        self.assertNotEqual(result,userControlErrValue["ERRwriteFile"],"ERRwriteFile in userDataInit")
        pass
    
    def testUserDataSaveAs(self):
        pass
#        result=self.userControl1.userDataSaveAs("d:\\test1.txt")
#        self.assertNotEqual(result,userControlErrValue["ERRopenFile"],"ERRopenFile in userDataInit")        
#        self.assertNotEqual(result,userControlErrValue["ERRwriteFile"],"ERRwriteFile in userDataInit")
        pass

               
def suite():
    suite=unittest.TestSuite()
    suite.addTest(testTxtUserControlTestCase('testAddDeleteuser'))
    suite.addTest(testTxtUserControlTestCase('testUserDataInit'))
    suite.addTest(testTxtUserControlTestCase('testAddDeleteUserFriend'))
    suite.addTest(testTxtUserControlTestCase('testcheckUser'))
    suite.addTest(testTxtUserControlTestCase('testUserDataSave'))
    suite.addTest(testTxtUserControlTestCase('testUserDataSaveAs'))
    return suite

#def suite():
#    suite=unittest.makeSuite(testTxtUserControlTestCase, 'test')
#    return suite
               
if __name__=="__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
    
#    unittest.main()       

## -*- coding: gb2312 -*-
#
#import sqlUserControl
#
#if __name__ == '__main__':
#    print "test userControl"
#    testUserControl=sqlUserControl.userControl("xiaodong","xd","apples")
##    testUserControl.findUser("xd")
##    userFriend=testUserControl.getUserFriends("xd")
#    testUserControl.addUser("linyu","lll")
#    print ""
#    testUserControl.deleteUser("linyu")
#    print ""
#    testUserControl.addUser("linyu1","lll")
#    print ""
#    testUserControl.deleteUser("linyu1")
#
#    testUserControl.close()