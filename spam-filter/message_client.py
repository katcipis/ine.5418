import os, sys, traceback, Ice

Ice.loadSlice(os.path.join('slices', 'Message.ice'))

import Messages


class ClientI(Messages.Client):

    def __init__(self, communicator):

        Messages.Client.__init__(self)
        try:
            # Create a proxy for the root directory
            obj = communicator.stringToProxy("MessagesServerInstance:default -p 10000")

            # Down-cast the proxy to a Directory proxy
            self.__server_prx = Messages.ServerPrx.checkedCast(obj)

        except:
            traceback.print_exc()
            print('ABORTING !!!')
            exit(-1)


    def receiveMessage(self, message, current=None):
        pass


    def receiveSpamBlacklist(self, blacklist, current=None):
        pass


class ClientApp(Ice.Application):

    def __init__(self, port):

        Ice.Application.__init__(self)
        self.__port = port


    def run(self, args):
        # Terminate cleanly on receipt of a signal
        self.shutdownOnInterrupt()

        # Create an object adapter (stored in the _adapter
        # static members)
        adapter = self.communicator().createObjectAdapterWithEndpoints("MessagesClient", 
                                                                       "default -p " + self.__port)
        ClientI._adapter = adapter
        client = ClientI(self.communicator())

        # All objects are created, allow client requests now
        adapter.activate()

        # Wait until we are done
        self.communicator().waitForShutdown()

        if self.interrupted():
            print self.appName() + ": terminating"

        return 0

if len(sys.argv) < 2:
    print('Usage: {0} port'.format(sys.argv[0]))
    exit()

print('Running client on port[{0}]'.format(sys.argv[1]))
app = ClientApp(sys.argv[1])
sys.exit(app.main(sys.argv))
