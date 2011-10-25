import os, sys, Ice

Ice.loadSlice(os.path.join('slices', 'Message.ice'))

import Messages


class ServerI(Messages.Server):

    def __init__(self, *args, **kwargs):

        Messages.Server.__init__(self, *args, **kwargs)
        self.__blacklist = []
        self.__clients = []


    def setAsSpam(self, message, current=None):

        self.__blacklist.append(message)
        print('\n-- -- -- SPAM BLACKLIST UPDATE -- -- --')
        for msg in self.__blacklist:
            print('domain[{0}] subject[{0}] body[{0}]')

        for client_prx in self.__clients:
            client_prx.receiveSpamBlacklist(self.__blacklist) 


    def register(self, client_prx, current=None):

        print('New messages client registered on the server')
        self.__clients.append(client_prx)



class ServerApp (Ice.Application):

    def run(self, args):
        # Terminate cleanly on receipt of a signal
        self.shutdownOnInterrupt()

        # Create an object adapter
        adapter = self.communicator().createObjectAdapterWithEndpoints("MessagesServer", "default -p 10000")
        server = ServerI()
        adapter.add(server, self.communicator().stringToIdentity("MessagesServerInstance"))

        # All objects are created, allow client requests now
        adapter.activate()

        # Wait until we are done
        self.communicator().waitForShutdown()

        if self.interrupted():
            print self.appName() + ": terminating"

        return 0


print('Running server')
app = ServerApp()
sys.exit(app.main(sys.argv))

