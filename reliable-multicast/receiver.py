
_BASE_PORT = 7777
_IP_ADDR   = '127.0.0.1'
_GROUP_PARTICIPANTS_FILENAME = 'group-participants.info'
_PARTICIPANT_SPLIT_STR = ':'


def get_group():
    group = []
    participants = open(_GROUP_PARTICIPANTS_FILENAME, 'r')

    for participant in _participants:
        ip, port = participant.split(_PARTICIPANT_SPLIT_STR)
        group.append({'ip':ip,'port':int(port)})

    participants.close()
    return group
    

def get_available_port (group):
    port = _BASE_PORT
    for participant in group:
        if participant['port'] == port:
            port += 1

    participants = open(_GROUP_PARTICIPANTS_FILENAME, 'a')
    participants.write(_IP_ADDR + _PARTICIPANT_SPLIT_STR + str(port) + '\n')
    participants.close()
    return port
        


if __name__ == '__main__':

    group = get_group()
    port = get_available_port(group)
    print('receiver process accepting connections at {ip}:{port}'.format(ip = _IP_ADDR, port=port))
