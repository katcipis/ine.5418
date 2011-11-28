import socket, traceback, log

_KEY_VALUE_SPLITTER = '='
_PAIR_SPLITTER = ':'


class MessageTransporter(object):

    def __init__(self, ip, port):
        log.log('MessageTransporter: ip[{0}] port[{1}]'.format(ip,port))

        self.__receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__receive_socket.bind((ip, port))
        self.__receive_socket.listen(1)


    def receive (self):
        conn, addr = self.__receive_socket.accept()
        data = conn.recv(4096) 
        conn.close()

        message = {}
        pairs = data.split(_PAIR_SPLITTER)
        for pair in pairs:
            k, v = pair.split(_KEY_VALUE_SPLITTER)
            message[k] = v

        return message
    

    def send(self, ip, port, message):
        serialized_message = ''
    
        for k,v in message.iteritems():
            serialized_message += str(k) + str(_KEY_VALUE_SPLITTER) + str(v) + str(_PAIR_SPLITTER)

        serialized_message = serialized_message[:-1]
        try:
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            send_socket.connect((ip, port))
            send_socket.send(serialized_message)
            send_socket.shutdown(socket.SHUT_RDWR)
            send_socket.close()
        except:
            log.log('MessageTransporter:send: unable to send message to ip[{0}] port[{1}]'.format(ip, port))
            traceback.log.log_exc()
