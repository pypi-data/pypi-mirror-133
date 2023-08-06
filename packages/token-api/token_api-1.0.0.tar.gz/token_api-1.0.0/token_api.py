import os
import sys
import time

class slowprint():
    def slowprint(s):
        for c in s + '\n':
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(1./10)
