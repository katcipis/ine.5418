import threading

_lock = threading.Lock()

def log(msg):
    global _lock
    with _lock:
        print(msg)
