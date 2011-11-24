from threading import Lock

_timestamp_lock = Lock()
_timestamp = 0

def update_timestamp(new_timestamp):
    _timestamp_lock.acquire()
    if new_timestamp > _timestamp:
        _timestamp = new_timestamp
    _timestamp_lock.release()

def get_timestamp():
    _timestamp_lock.acquire()
    aux = _timestamp
    _timestamp_lock.release()
    return aux
