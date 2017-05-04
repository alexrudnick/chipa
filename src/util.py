import time
import sys
from datetime import datetime

DPRINT=True
def dprint(*a,**aa):
    if DPRINT:
        print(file=sys.stderr, *a, **aa)

class timeexecution():
    """Function decorator for timing a function."""
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        dprint("Entering", self.f.__name__)
        starttime = time.time()
        out = self.f(*args, **kwargs)
        dprint("Exiting {0}, {1:.2f} sec later".
              format(self.f.__name__, time.time() - starttime))
        return out

def timestamp():
    now = datetime.now()
    return ("%4d-%02d-%02d-%02d-%02d" % (now.year, now.month, now.day, now.hour,
                                         now.minute))
