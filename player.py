#!/usr/bin/python3
import sys
import pickle
from time import time

sys.argv.pop(0)                                                 #
fp = sys.argv.pop(0)                                            # first arg is project path
pis = []
for arg in sys.argv:
        pis.append(int(arg))

try:
    f = open(fp, "rb")
    cproj = pickle.load(f)
    tempo = cproj.getTempo()
    tn = time()
    i = 0
    while True:
        while time()-tn < i*(60/tempo):
            pass
        d = ""
        for pi in pis:
            if not cproj.patterns[pi].muted:
                d = d + " " + str(cproj.playerRead(pi, i))
        sys.stdout.write(d[1:] + "\n")                          # first char is always space
        sys.stdout.flush()
        i = i + 1
except KeyboardInterrupt:
    pass
