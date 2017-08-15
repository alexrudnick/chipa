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

def save_results_table(results_table, fn):
    with open(fn, "w") as outfile:
        ## one entry into these per word
        corrects = []
        mfscorrects = []
        sizes = []
        for w, resultslist in results_table.items():
            for (correct,size) in resultslist:
                print("{0}\t{1}\t{2}\t{3}".format(
                    w, correct / size, correct, size), file=outfile)
                corrects.append(correct)
                sizes.append(size)
        avg = sum(corrects) / sum(sizes)
        print("accuracy: {0:.4f}".format(avg), file=outfile)
