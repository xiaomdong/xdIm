# -*- coding: UTF-8 -*-
'''
Created on 2010-10-25

@author: x00163361
'''

from server_twisted import *
from twisted.application import internet,sservice
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile

port = 8001

factory = xdServerFactory(None)
# this is the important bit
application = service.Application("xdImServer") # create the Application
xdImService = internet.TCPServer(port, factory) # create the service
# add the service to the application
xdImService.setServiceParent(application)