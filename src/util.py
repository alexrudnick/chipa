import time
import sys

DPRINT=False
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
