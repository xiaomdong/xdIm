'''
Created on 2011-1-25

@author: x00163361
'''
from serverManager import *
from PySide.QtTest import *


#class TestGui(QObject):
#    def testGui(self):
#        testWin=serverManagerWindow(None)
#        QTest.mouseClick(testWin.ui.startServer_pushButton,Qt.LeftButton)
        
class testQString(QObject):
    def initTestCase(self):
        print "initTestCase"
        
    
    def clearupTestCase(self):
        print "clearupTestCase"

    def toUpper(self):
        str="Hello"
        print "toUpper"

if __name__ == '__main__':
    x=testQString()
#    x.testGui()


            