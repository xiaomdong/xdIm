from client.client_twisted import *

if __name__ =="__main__":
    host="localhost"
    port=8001
    clientConnector=0
    connecting=runClient(host,port,"xd","apples")
    connecting.addCallback(handelSuccess,port)
    connecting.addErrback(handelFailure,port)
    reactor.run()