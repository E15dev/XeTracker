import hd

def empty(count, name):
    return hd.TrProject(count, name)

def random(count, name):
    from random import random
    from math import floor
    d = hd.TrProject(count, name)
    for i in range(count):
        for j in range(64):
            d.write(i, j, floor(random()*12))
    return d

def instrumentSine():
    return hd.instrument(0x57, b'x00')
