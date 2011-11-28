import threading, timestamp, random, time, log


class MulticastSender (object):
  
    def __init__(self, proc_id, group, transporter):
        self.__proc_id = proc_id
        self.__group = group
        self.__transporter = transporter


    def reliable_multicast (self, msg):
        for proc in self.__group:
            log.log('MulticastSender: sending msg[{msg}] to ip[{ip}] port[{port}]'.format(msg=msg, ip=proc['ip'], port=proc['port']))
            self.__transporter.send(proc['ip'], proc['port'], msg)


    def atomic_multicast (self, msg):
        #Lets append the id + timestamp
        log.log('MulticastSender: multicasting message[{0}]'.format(msg))
        self.reliable_multicast ({'timestamp':timestamp.get_timestamp(),
                                  'id':self.__proc_id,
                                  'message':msg })


class Sender(threading.Thread):

    def __init__(self, proc_id, group, messages_count, transporter):
        threading.Thread.__init__(self)
        self.__messages_count = messages_count
        self.__multicast_sender = MulticastSender(proc_id, group, transporter)


    def run (self):
        log.log('Sender: starting')
        for i in range(self.__messages_count):
            log.log('Sender: sending message ' + str(i))
            self.__multicast_sender.atomic_multicast("message {0}".format(i))
            time.sleep(random.random())

        log.log('Sender: ending')

