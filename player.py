#!/usr/bin/python3
import sys
import pickle
from time import time

fp = sys.argv[1]
pi = int(sys.argv[2])

try:
    f = open(fp, "rb")
    cproj = pickle.load(f)
    tempo = cproj.getTempo()
    tn = time()
    i = 0
    while True:
        while time()-tn < i*(60/tempo):
            pass
        sys.stdout.write(str(cproj.playerRead(pi, i)) + "\n")
        sys.stdout.flush()
        i = i + 1
except KeyboardInterrupt:
    pass
