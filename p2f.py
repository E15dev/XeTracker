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

def convert(p: int):
    oct = p // 12
    mp = p % 12
    return bfqs[mp]*(pow(2, oct))


if __name__ == "__main__":
    import sys
    try:
        while True:
            p = sys.stdin.readline()[:-1]   # cut "\n" from end
            if p == "":
                raise KeyboardInterrupt     # probably i will need to add printing something on end so sound gen with know that it also needs to stop
            print(convert(int(p)))
    except KeyboardInterrupt:
        pass
