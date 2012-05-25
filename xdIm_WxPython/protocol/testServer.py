from server.server_twisted import *

if __name__ =="__main__":
    port=8001
    connecting=runServer(port)
    connecting.addCallback(handelSuccess,port)
    connecting.addErrback(handelFailure,port)
    reactor.run()