import os, sys, traceback, Ice
import message_server

Ice.loadSlice(os.path.join('slices', 'Message.ice'))

import Messages


class ClientI(Messages.Client):

    def __init__(self, communicator, adapter):

        Messages.Client.__init__(self)
        self.__blacklist = []
        self.__received_messages = []

        try:
            # Create a proxy for the server
            obj = communicator.stringToProxy("MessagesServerInstance:default -h {0} -p {1}".format(message_server.SERVER_HOST, message_server.SERVER_PORT))

            # Down-cast the proxy to a Server proxy
            self.__server_prx = Messages.ServerPrx.checkedCast(obj)

            # Create an identity - cant be a UUID since we must create a proxy on the sender
            self._id = Ice.Identity()
            self._id.name = 'MessagesClientInstance'
           
            #create a proxy for this client
            self.__client_prx = Messages.ClientPrx.uncheckedCast(adapter.add(self, self._id))
            #register ourselves on the server ;-)
            self.__server_prx.register(self.__client_prx)

        except:
            traceback.print_exc()
            print('ABORTING !!!')
            exit(-1)


    def receiveMessage(self, message, current=None):
        print('\nreceiveMessage: message domain[{m.domain}] subject[{m.subject}] body[{m.body}]'.format(m = message))
        if message.domain in self.__blacklist:
            print('receiveMessage: the message domain is marked as SPAM !!!')
            return

        for received_message in self.__received_messages:
            if (message.subject == received_message.subject and
                message.body == received_message.body):

                print('receiveMessage: detected a SPAM message')
                print('receiveMessage: blacklisting domain {0}'.format(message.domain))
                self.__server_prx.setAsSpam(message)
                if message.domain != received_message.domain:
                    print('receiveMessage: also blacklisting domain {0}'.format(received_message.domain))
                    self.__server_prx.setAsSpam(received_message)
                return

        print('receiveMessage: message is not spam')
        self.__received_messages.append(message)
                

    def receiveSpamBlacklist(self, blacklist, current=None):
        if blacklist == []:
            return

        self.__blacklist = [message.domain for message in blacklist]
        print('\n-- -- -- BLACKLISTED DOMAINS UPDATE -- -- --')
        for domain in self.__blacklist:
            print(domain)


class ClientApp(Ice.Application):

    def __init__(self, host, port):

        Ice.Application.__init__(self)
        self.__port = port
        self.__host = host


    def run(self, args):
        # Terminate cleanly on receipt of a signal
        self.shutdownOnInterrupt()

        # Create an object adapter
        adapter = self.communicator().createObjectAdapterWithEndpoints("MessagesClient", 
                                                                       "default -h {0} -p {1}".format(self.__host, self.__port))
        client = ClientI(self.communicator(), adapter)

        # All objects are created, allow client requests now
        adapter.activate()

        # Wait until we are done
        self.communicator().waitForShutdown()

        if self.interrupted():
            print self.appName() + ": terminating"

        return 0


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print('Usage: {0} host port'.format(sys.argv[0]))
        exit()

    print('Running client on host[{0}] port[{1}]'.format(sys.argv[1], sys.argv[2]))
    app = ClientApp(sys.argv[1], sys.argv[2])
    sys.exit(app.main(sys.argv))

