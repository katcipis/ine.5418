from threading import Lock

_timestamp_lock = Lock()
_timestamp = 0

def update_timestamp(new_timestamp):
    with _timestamp_lock:
        if new_timestamp > _timestamp:
            _timestamp = new_timestamp

def get_timestamp():
    with _timestamp_lock:
        aux = _timestamp
    return aux
