import time, collections, atexit, pprint
PROFILE = collections.Counter()

class TimeRecorder(object):
    def __init__(self, key):
        self.key = key
    def __enter__(self):
        self.start = time.time()
    def __exit__(self, *a):
        PROFILE[self.key] += (time.time() - self.start)

def print_time():
    pprint.pprint(dict(PROFILE))

#atexit.register(print_time)
