from threading import Lock

_timestamp_lock = Lock()
_timestamp = 0

def update_timestamp(new_timestamp):
    #the exact opposite of lua :-)
    global _timestamp
    global _timestamp_lock

    with _timestamp_lock:
        if new_timestamp > _timestamp:
            _timestamp = new_timestamp

def get_timestamp():
    #the exact opposite of lua :-)
    global _timestamp
    global _timestamp_lock

    with _timestamp_lock:
        aux = _timestamp
        _timestamp += 1
    return aux
