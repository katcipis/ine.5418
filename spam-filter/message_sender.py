import os, sys, traceback, Ice

Ice.loadSlice(os.path.join('slices', 'Message.ice'))

import Messages


class SenderApp(Ice.Application):

    def __init__(self, host, port, domain, title, body):

        Ice.Application.__init__(self)
        self.__port = port
        self.__host = host
        self.__message = Messages.Msg()
        self.__message.domain  = domain
        self.__message.subject = title
        self.__message.body    = body


    def run(self, args):
        # Terminate cleanly on receipt of a signal
        self.shutdownOnInterrupt()

        # Create a proxy for the server
        obj = self.communicator().stringToProxy("MessagesClientInstance:default -h {0} -p {1}".format(self.__host, self.__port))

        # Down-cast the proxy to a Server proxy
        message_client_prx = Messages.ClientPrx.checkedCast(obj)

        #send the message
        message_client_prx.receiveMessage(self.__message)

        # Wait until we are done
        self.communicator().waitForShutdown()

        if self.interrupted():
            print self.appName() + ": terminating"

        return 0


if len(sys.argv) < 6:
    print('Usage: {0} host port domain title body'.format(sys.argv[0]))
    exit()

print('Sending message to client on host[{0}] port[{1}]'.format(sys.argv[1], sys.argv[2]))
app = SenderApp(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
sys.exit(app.main(sys.argv))
