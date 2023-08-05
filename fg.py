import hd

def empty(count, name):
    return hd.TrFile(count, name)

def random(count, name):
    from random import random
    from math import floor
    d = hd.TrFile(count, name)
    for i in range(count):
        for j in range(64):
            d.write(i, j, floor(random()*12))
    return d
