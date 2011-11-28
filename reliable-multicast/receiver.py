import threading


class Receiver(threading.Thread):

    def __init__(self, proc_id, receive_msgs_count):
        threading.Thread.__init__(self)
        self.__receive_msgs_count = receive_msgs_count
        self.__proc_id = proc_id

    def run (self):
        pass
