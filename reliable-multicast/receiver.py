import socket
import config


def wait_for_start (ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(1)

    conn, addr = sock.accept()
    data = conn.recv(1024) #whatever, just a start ping
    conn.close()


if __name__ == '__main__':

    group = config.get_group()
    port = config.get_available_port(group)
    config.insert_proc_on_group (port)
    proc_id = config.get_uuid()
    ip = config.get_ip() 

    print('process {proc_id} waiting for start at {ip}:{port}'.format(ip = ip, port=port, proc_id = proc_id))
    wait_for_start(ip, port)
    print('starting process {proc_id}'.format(proc_id = proc_id))
