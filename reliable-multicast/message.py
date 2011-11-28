import socket, traceback, log

_KEY_VALUE_SPLITTER = '='
_PAIR_SPLITTER = ':'


class MessageTransporter(object):

    def __init__(self, ip, port):
        log.log('MessageTransporter: ip[{0}] port[{1}]'.format(ip,port))

        self.__receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__receive_socket.bind((ip, port))
        self.__receive_socket.listen(128)


    def __del__(self):
        self.__receive_socket.shutdown(socket.SHUT_RDWR)
        self.__receive_socket.close()


    def receive (self):
        log.log('MessageTransporter: accepting connection')
        conn, addr = self.__receive_socket.accept()
        log.log('MessageTransporter: accepted connection')
        data = conn.recv(4096) 
        log.log('MessageTransporter: received data[{0}]'.format(data))
        conn.close()

        msg = {}
        pairs = data.split(_PAIR_SPLITTER)
        for pair in pairs:
            k, v = pair.split(_KEY_VALUE_SPLITTER)
            msg[k] = v

        log.log('MessageTransporter: received message[{0}]'.format(msg))
        return msg
    

    def send(self, ip, port, message):
        serialized_message = ''
    
        for k,v in message.iteritems():
            serialized_message += str(k) + str(_KEY_VALUE_SPLITTER) + str(v) + str(_PAIR_SPLITTER)

        serialized_message = serialized_message[:-1]
        try:
            log.log('MessageTransporter:send: sending message[{0}]'.format(message))
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            send_socket.connect((ip, port))
            send_socket.send(serialized_message)
            send_socket.close()
            log.log('MessageTransporter:send: success sending message[{0}]'.format(message))
        except:
            log.log('MessageTransporter:send: unable to send message to ip[{0}] port[{1}]'.format(ip, port))
            traceback.print_exc()
