# -*- coding: UTF-8 -*-
'''
Created on 2010-9-19

@author: x00163361
'''


from debug import *
from config import *
import unittest



class testconfigTestCase(unittest.TestCase):
    def setUp(self):
        self.Config=serverConfig("test.cfg")
        pass
    
    def tearDown(self):
        
        pass
    
    
    def testXmlContrl(self):
        self.Config.setContrlMedia("xml")
        self.assertEqual("xml",self.Config.getControlMedia())

    def testTxtContrl(self):
        self.Config.setContrlMedia("txt")
        self.assertEqual("txt",self.Config.getControlMedia())

    def testMysqlContrl(self):
        self.Config.setContrlMedia("mysql")
        self.assertEqual("mysql",self.Config.getControlMedia())

    
    def testWrongContrl(self):
        self.Config.setContrlMedia("ttttt")        
        self.assertNotEqual("tttt",self.Config.getControlMedia(),"OK in testWrongContrl")
            
    

def suite():
    suite=unittest.TestSuite()
    suite.addTest(testconfigTestCase('testXmlContrl'))
    suite.addTest(testconfigTestCase('testTxtContrl'))
    suite.addTest(testconfigTestCase('testMysqlContrl'))
    suite.addTest(testconfigTestCase('testWrongContrl'))
    return suite

#def suite():
#    suite=unittest.makeSuite(testXmlUserControlTestCase, 'test')
#    return suite
               
if __name__=="__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
    
#    unittest.main()    