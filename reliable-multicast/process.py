#!/usr/bin/env python

import socket, config, message

if __name__ == '__main__':

    group = config.get_group()
    port = config.get_available_port(group)
    config.insert_proc_on_group (port)
    proc_id = config.get_uuid()
    ip = config.get_ip() 

    print('process {proc_id} waiting for start at {ip}:{port}'.format(ip = ip, port=port, proc_id = proc_id))
    start_message = message.receive(ip, port)
    print('{proc_id} received {msg}'.format(proc_id = proc_id, msg = start_message))
