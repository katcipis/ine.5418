import os 

_BASE_PORT = 7777
_IP_ADDR   = '127.0.0.1'
_GROUP_PARTICIPANTS_FILENAME = 'group-participants.info'
_PARTICIPANT_SPLIT_STR = ':'


def get_ip():
    return _IP_ADDR


def reset_group():
    try:
        os.remove(_GROUP_PARTICIPANTS_FILENAME)    
    except:
        pass


def get_group():
    group = []
   
    try:
        participants = open(_GROUP_PARTICIPANTS_FILENAME, 'r')
    except IOError:
        return group

    for participant in participants:
        ip, port = participant.split(_PARTICIPANT_SPLIT_STR)
        group.append({'ip':ip,'port':int(port)})

    participants.close()
    return group


def get_available_port ():
    group = get_group()
    port = _BASE_PORT
    for participant in group:
        if participant['port'] == port:
            port += 1

    return port


def get_uuid():
    return len(get_group())


def insert_proc_on_group(port):
    participants = open(_GROUP_PARTICIPANTS_FILENAME, 'a')
    participants.write(_IP_ADDR + _PARTICIPANT_SPLIT_STR + str(port) + '\n')
    participants.close()
