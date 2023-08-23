#!/usr/bin/python3
import sys
import pickle
from time import time

sys.argv.pop(0)                                                 # pop path
fp = sys.argv.pop(0)                                            # project name
pids = []
for arg in sys.argv:
        pids.append(int(arg))                                   # args that left are patterns ids

try:
    f = open(fp, "rb")
    cproj = pickle.load(f)
    if pids == []:                                               # if no patterns specified, it will play all not muted
        pids = range(len(cproj.patterns))
    tempo = cproj.getTempo()
    tn = time()
    i = 0
    while True:
        while time()-tn < i*(60/tempo):
            pass
        d = ""
        for pi in pids:
            if not cproj.patterns[pi].muted:
                d = d + " " + str(cproj.playerRead(pi, i))
        sys.stdout.write(d[1:] + "\n")                          # first char is always space
        sys.stdout.flush()
        i = i + 1
except KeyboardInterrupt:
    pass
