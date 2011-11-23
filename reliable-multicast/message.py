import socket

def send(ip, port, message):
    serialized_message = ''
    
    for k,v in message.iteritems():
        serialized_message += k + '=' + v + ':'

    serialized_message = serialized_message[:-1]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(serialized_message)
    s.close()
