#!/usr/bin/env python

import config, sys
from message import MessageTransporter


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('usage: {0} <messages to be sent by each process>'.format(sys.argv[0]))
        exit()

    group = config.get_group()
    messages = sys.argv[1]
    message_trans = MessageTransporter('127.0.0.1', config._BASE_PORT - 1)

    print('starting processes to send {0} messages each'.format(messages))

    for participant in group:
        print('sending start to {ip}:{port}'.format(ip = participant['ip'], port = participant['port']))
        message_trans.send(participant['ip'], participant['port'], {'start':messages})

    print('done')
