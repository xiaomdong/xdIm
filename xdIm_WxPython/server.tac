#twistd -ny server.tac

import os
from twisted.application import service, internet
from twisted.web import static, server
import sys
sys.path.append(os.getcwd())
from protocol.server.server_twisted import xdServerFactory
from twisted.internet.protocol import ServerFactory

def getWebService():
	"""
	Return a service suitable for creating an application object.
	This service is a simple web server that serves files on port 8080 from
	underneath the current working directory.
	"""
	# create a resource to serve static files
	#fileServer = server.Site(static.File(os.getcwd()))
	return internet.TCPServer(8001, xdServerFactory())
# this is the core part of any tac file, the creation of the root-level
# application object

application = service.Application("Demo application")
# attach the service to its parent application
service = getWebService()
service.setServiceParent(application)