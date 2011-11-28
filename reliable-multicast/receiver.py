import threading, timestamp, log


class LamportMessage(object):

    def __init__ (self, msg):
        self._id = msg['id']
        self._timestamp = msg['timestamp']
        self._message = msg['message']

    def __cmp__(self, other):

        if self._timestamp < other._timestamp:
            return -1
        if self._timestamp > other._timestamp:
            return 1
        if self._id < other._id:
            return -1
        if self._id > other._id:
            return 1
        return 0


class MulticastReceiver(object):


    def __init__(self, proc_id, group, transporter):
        self.__proc_id = proc_id
        self.__group = group
        self.__msgs_buffer = []
        self.__lamport_msgs = []
        self.__transporter = transporter


    def get_messages_on_arrival_order(self):
        return self.__msgs_buffer


    def get_messages_ordered(self):
        #lamport algorithm. The comparison is made on LamportMessage.
        self.__lamport_msgs.sort()
        return self.__lamport_msgs


    def atomic_deliver(self, msg):
        self.__lamport_msgs.append(LamportMessage(msg))
        if (msg['id'] != self.__proc_id):
            timestamp.update_timestamp(int(msg['timestamp']))


    def reliable_deliver(self, msg):
        if msg in self.__msgs_buffer:
            log.log('MulticastReceiver: already received message[{0}]'.format(msg))
            return

        self.__msgs_buffer.append(msg)
        self.atomic_deliver(msg)

        log.log('MulticastReceiver: received new message[{0}], multicasting it'.format(msg))
        for proc in self.__group:
            self.__transporter.send(proc['ip'], proc['port'], msg)

        log.log('MulticastReceiver: done')


    def received_msgs_size(self):
        return len(self.__msgs_buffer)



class Receiver(threading.Thread):


    def __init__(self, proc_id, group, receive_msgs_count, transporter):
        threading.Thread.__init__(self)
        self.__receive_msgs_count = receive_msgs_count
        self.__receiver = MulticastReceiver(proc_id, group, transporter)
        self.__transporter = transporter


    def run (self):
        log.log('Receiver: starting')
        while (self.__receiver.received_msgs_size() != self.__receive_msgs_count):
            log.log('Receiver: received [{0}] msgs expect [{1}] msgs'.format(self.__receiver.received_msgs_size(), self.__receive_msgs_count))
            msg = self.__transporter.receive()
            log.log('Receiver: received [{0}] msgs expect [{1}] msgs'.format(self.__receiver.received_msgs_size(), self.__receive_msgs_count))
            self.__receiver.reliable_deliver(msg)
            log.log('Receiver: received [{0}] msgs expect [{1}] msgs'.format(self.__receiver.received_msgs_size(), self.__receive_msgs_count))
            
