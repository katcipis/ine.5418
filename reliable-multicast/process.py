#!/usr/bin/env python

import socket, config, message
import sender, receiver

if __name__ == '__main__':

    group = config.get_group()
    port = config.get_available_port(group)
    config.insert_proc_on_group (port)
    proc_id = config.get_uuid()
    ip = config.get_ip() 

    print('process {proc_id} waiting for start at {ip}:{port}'.format(ip = ip, port=port, proc_id = proc_id))
    start_message = message.receive(ip, port)
    print('{proc_id} received start message:[{msg}]'.format(proc_id = proc_id, msg = start_message))

    #starting sender thread
    send_msgs_count = int(start_message['start'])
    sender = sender.Sender(proc_id, group, send_msgs_count)
    sender.start()

    #starting receiver thread
    received_msgs_count = (len(group) + 1) * send_msgs_count
    receiver = receiver.Receiver(proc_id, received_msgs_count)
    receiver.start()
    receiver.join()

    print('process {proc_id} exited successfully'.format(proc_id = proc_id))
