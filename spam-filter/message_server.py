import os, sys, Ice

Ice.loadSlice(os.path.join('slices', 'Message.ice'))

import Messages

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 10000

class ServerI(Messages.Server):

    def __init__(self, *args, **kwargs):
        Messages.Server.__init__(self, *args, **kwargs)
        self.__blacklist = []
        self.__clients = []


    def setAsSpam(self, message, current=None):
        for blacklisted_msg in self.__blacklist:
            if (blacklisted_msg.domain == message.domain and 
                blacklisted_msg.subject == message.subject and 
                blacklisted_msg.body == message.body): 
                return

        self.__blacklist.append(message)
        print('\n-- -- -- SPAM BLACKLIST UPDATE -- -- --')
        for msg in self.__blacklist:
            print('domain[{m.domain}] subject[{m.subject}] body[{m.body}]'.format(m = msg))

        for client_prx in self.__clients:
            client_prx.begin_receiveSpamBlacklist(self.__blacklist) 


    def register(self, client_prx, current=None):
        print('register: new MessagesClient registered on the server')
        self.__clients.append(client_prx)
        client_prx.begin_receiveSpamBlacklist(self.__blacklist)



class ServerApp (Ice.Application):

    def run(self, args):
        # Terminate cleanly on receipt of a signal
        self.shutdownOnInterrupt()

        # Create an object adapter
        adapter = self.communicator().createObjectAdapterWithEndpoints("MessagesServer", "default -h {0} -p {1}".format(SERVER_HOST, SERVER_PORT))
        server = ServerI()
        # The server id must be well know and human readable (not a UUID)
        adapter.add(server, self.communicator().stringToIdentity("MessagesServerInstance"))

        # All objects are created, allow client requests now
        adapter.activate()

        # Wait until we are done
        self.communicator().waitForShutdown()

        if self.interrupted():
            print self.appName() + ": terminating"

        return 0


if __name__ == '__main__':
    print('Running server')
    app = ServerApp()
    sys.exit(app.main(sys.argv))

