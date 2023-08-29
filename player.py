#!/usr/bin/python3
import sys
from time import time
import p2f
from tx import OD
from cf import readProj, saveProj

sys.argv.pop(0)                                                 # pop path
fp = sys.argv.pop(0)                                            # project name
pids = []
for arg in sys.argv:
        pids.append(int(arg))                                   # args that left are patterns ids

try:
    cproj = readProj(fp)
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
                # vol freq instrument automation
                note = cproj.patterns[pi].notes[cproj.patterns[pi].playerIndex(i)]
                d += " " + str(note.vol/255) + " " + str(p2f.convert(note.pitch)) + " " + str(cproj.patterns[pi].instrument) + " " + "0"
        sys.stdout.write(d[1:] + "\n")                          # first char is always space
        sys.stdout.flush()
        i = i + 1
except AttributeError:
    print(OD)
except KeyboardInterrupt:
    pass
