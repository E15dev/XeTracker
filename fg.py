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

def instrumentTriangle():
    eb, wave, full = bytes(), bytes(), bytes()

    for i in range(32): # 127 to 255
        wave = eb.join([wave, int(127 + i*4).to_bytes(1, "big", signed=False)])
    for i in range(64): # 255 to 0
        wave = eb.join([wave, int(255-(i*4)).to_bytes(1, "big", signed=False)])
    for i in range(31): # 0 to 127
        wave = eb.join([wave, int(i*4).to_bytes(1, "big", signed=False)])

    full = eb.join([full, b'\xff']) # full interpolation
    full = eb.join([full, wave])    # waveform 0
    full = eb.join([full, wave])    # waveform 1
    return hd.TrInstrument(0x77, full) # "w" for new wavetable format and then wavetable data
