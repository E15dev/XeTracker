#!/usr/bin/python3
# this is program to conver pitch from XeTracker to frequency

bfqs = [
440.0,                          # a
466.16,                         # a#
493.88,                         # b
523.25,                         # c
554.37,                         # c#
587.33,                         # d
622.25,                         # d#
659.25,                         # e
698.46,                         # f
739.99,                         # f#
783.99,                         # g
830.61]                         # g#

import sys

try:
    while True:
        v = sys.stdin.readline()[:-1]
        if v == "":
            raise KeyboardInterrupt
       	v = int(v)              # TODO: GET VAL THAT WILL BE PIPED FROM PLAYER
        oct = v // 12           # get octave
        mp = v % 12             # get base pitch (always in 0 oct)
        print(bfqs[mp]*(pow(2, oct)))
except KeyboardInterrupt:
    pass
