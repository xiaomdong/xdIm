# -*- coding: UTF-8 -*-

from txtUserControl import *
import unittest

class testTxtUserControlTestCase(unittest.TestCase):
    def setUp(self):
        self.userControl1=txtUserControl("d:\\xxx.txt")
        self.userControl1.userDataInit()
        self.saveUserFriends=self.userControl1.userFriends
        self.saveUserPassword=self.userControl1.userPassword
    
    def tearDown(self):
        self.userControl1.userFriends=self.saveUserFriends
        self.userControl1.userPassword=self.saveUserPassword
        self.userControl1.exit()
        pass
    
    def testUserDataInit(self):
        self.userControl1.userDataSave()
        result=self.userControl1.userDataInit()
        self.assertEqual(result,userControlErrValue["OK"],"Error in userDataInit")
        pass
    
    def testAddDeleteuser(self):
        if self.userControl1.findUser("cc")!=userControlErrValue["HaveUser"]:
            pass
        else:
            result=self.userControl1.deleteUser("cc")
            self.assertEqual(result,userControlErrValue["OK"],"OK in deleteUser")
                
        result=self.userControl1.addUser("cc", "apples")
        self.assertEqual(result,userControlErrValue["OK"],"OK in addUser")
        result=self.userControl1.deleteUser("cc")
        self.assertEqual(result,userControlErrValue["OK"],"OK in deleteUser")
    
    def testAddDeleteUserFriend(self):
        if self.userControl1.findUser("cc")!=userControlErrValue["HaveUser"]:
            pass
        else:
            self.userControl1.deleteUser("cc")
        
        if self.userControl1.findUser("mm")!=userControlErrValue["HaveUser"]:
            pass
        else:
            self.userControl1.deleteUser("mm")
            
        self.userControl1.addUser("cc", "apples")
        self.userControl1.addUser("mm", "apples")
            
        result=self.userControl1.addUserFriend("cc", "mm")
        self.assertEqual(result,userControlErrValue["OK"],"OK in addUserFriend")
        result=self.userControl1.deleteUserFriend("cc", "mm")
        self.assertEqual(result,userControlErrValue["OK"],"OK in deleteUserFriend")
        
        self.userControl1.deleteUser("cc")
        self.userControl1.deleteUser("mm")
            
    def testcheckUser(self):
        self.userControl1.addUser("cc", "apples")
        
        result=self.userControl1.checkUser("cc", "apples")
        self.assertEqual(result,userControlErrValue["OK"],"OK in checkUser")
        
        result=self.userControl1.checkUser("cc", "cvs")
        self.assertEqual(result,userControlErrValue["UserPasswordErr"],"UserPasswordErr in checkUser")
        
        self.userControl1.deleteUser("cc")
        
        result=self.userControl1.checkUser("cc", "apples")
        self.assertEqual(result,userControlErrValue["NoUser"],"NoUser in checkUser")
    
    def testUserDataSave(self):
        self.userControl1.addUser("cc", "apples")
        self.userControl1.addUser("mm", "apples")
        self.userControl1.addUserFriend("cc", "mm")
        result=self.userControl1.userDataSave()
        self.assertNotEqual(result,userControlErrValue["ERRopenFile"],"ERRopenFile in userDataInit")        
        self.assertNotEqual(result,userControlErrValue["ERRwriteFile"],"ERRwriteFile in userDataInit")
        self.userControl1.deleteUser("cc")
        self.userControl1.deleteUser("mm")
        self.assertNotEqual(result,userControlErrValue["ERRopenFile"],"ERRopenFile in userDataInit")        
        self.assertNotEqual(result,userControlErrValue["ERRwriteFile"],"ERRwriteFile in userDataInit")
        pass
    
    def testUserDataSaveAs(self):
        result=self.userControl1.userDataSaveAs("d:\\test1.txt")
        self.assertNotEqual(result,userControlErrValue["ERRopenFile"],"ERRopenFile in userDataInit")        
        self.assertNotEqual(result,userControlErrValue["ERRwriteFile"],"ERRwriteFile in userDataInit")
        pass

               
def suite():
    suite=unittest.TestSuite()
#    suite.addTest(testTxtUserControlTestCase('testAddDeleteuser'))
    suite.addTest(testTxtUserControlTestCase('testUserDataInit'))
#    suite.addTest(testTxtUserControlTestCase('testAddDeleteUserFriend'))
#    suite.addTest(testTxtUserControlTestCase('testcheckUser'))
#    suite.addTest(testTxtUserControlTestCase('testUserDataSave'))
#    suite.addTest(testTxtUserControlTestCase('testUserDataSaveAs'))
    return suite

#def suite():
#    suite=unittest.makeSuite(testTxtUserControlTestCase, 'test')
#    return suite
               
if __name__=="__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
    
#    unittest.main()       