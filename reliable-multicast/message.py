import socket

_KEY_VALUE_SPLITTER = '='
_PAIR_SPLITTER = ':'

def receive (ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(1)

    conn, addr = sock.accept()
    data = conn.recv(4096) 
    conn.close()

    message = {}
    pairs = data.split(_PAIR_SPLITTER)
    for pair in pairs:
        k, v = pair.split(_KEY_VALUE_SPLITTER)
        message[k] = v

    return message
    

def send(ip, port, message):
    serialized_message = ''
    
    for k,v in message.iteritems():
        serialized_message += k + str(_KEY_VALUE_SPLITTER) + v + str(_PAIR_SPLITTER)

    serialized_message = serialized_message[:-1]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(serialized_message)
    s.close()
