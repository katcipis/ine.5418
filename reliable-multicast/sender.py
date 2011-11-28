import threading
import timestamp, message

class MulticastSender (object):
  
    def __init__(self, proc_id, group):
        self.__proc_id = proc_id
        self.__group = group


    def reliable_multicast (self, msg):
        for proc in self.__group:
            message.send(proc['ip'], proc['port'], msg)


    def atomic_multicast (self, message):
        #Lets append the id + timestamp
        self.reliable_multicast ({'timestamp':timestamp.get_timestamp(),
                                  'id':self.__proc_id,
                                  'message':message })


class Sender(threading.Thread):

    def __init__(self, proc_id, group, messages_count):
        threading.Thread.__init__(self)
        self.__messages_count = messages_count
        self.__multicast_sender = MulticastSender(proc_id, group)


    def run (self):
        for i in range(self.__messages_count):
            self.__multicast_sender.atomic_multicast("message {0}".format(i))

