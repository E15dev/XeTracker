#!/bin/python3
import sys
import hd
from struct import pack
from struct import unpack

class TooBig(Exception):
    pass

class InvalidSignature(Exception):
    pass

class ProjectTooOld(Exception):
    pass

class ProjectTooNew(Exception):
    pass

def pr(s, l: int, b: str):
    if len(str(s)) > l:
        raise TooBig
    return str(s) + b*((l-len(str(s)))//len(b))

def pl(s, l: int, b: str):
    if len(str(s)) > l:
        raise TooBig
    return b*((l-len(str(s)))//len(b)) + str(s)

def iToI(i, s: bool, size=1):
    return int().from_bytes(i.to_bytes(size, bo), bo, signed=s)

########################################################################################
def InstrumentGetEmpty():
    return ("P" + sp*255).encode()  # it can be anything that starts with "P"

########################################################################################
def InstrumentToClass(d: bytes):
    if len(d) > 256:
        raise OverflowError
    return hd.TrInstrument(iToI(d[0], False, 1), d[1:])

def InstrumentFromClass(c: hd.TrInstrument):
    g = bytes()
    g = eb.join([g, c.type.to_bytes(1, bo, signed=False)])
    g = eb.join([g, c.data])
    return g

def NoteToClass(d: bytes):
    return hd.TrNote(vol=iToI(d[0], False, 1), pitch=iToI(d[1], True, 1))

def NoteFromClass(c: hd.TrNote):
    g = bytes()
    g = eb.join([g, c.vol.to_bytes(1, bo, signed=False)])   # 1 byte
    g = eb.join([g, c.pitch.to_bytes(1, bo, signed=True)])  # 1 byte
    return g

def PatternToClass(d: bytes):
    p = hd.TrPattern()
    p.locked = bool(iToI(d[0], False, 1))
    p.muted = bool(iToI(d[1], False, 1))
    p.prlen = iToI(d[2], False, 1)
    p.proffset = iToI(d[3], False, 1)
    p.poffset = iToI(d[4], True, 1)
    p.instrument = iToI(d[5], False, 1)
    d = d[6:]
    for i in range(hd.MPL):
        p.notes[i] = NoteToClass(d[i*2:(i*2)+2])
    return p;

def PatternFromClass(c: hd.TrPattern):
    p = bytes()
    p = eb.join([p, c.locked.to_bytes(1, bo, signed=False)])        # 1 byte
    p = eb.join([p, c.muted.to_bytes(1, bo, signed=False)])         # 1 byte
    p = eb.join([p, c.prlen.to_bytes(1, bo, signed=False)])         # 1 byte
    p = eb.join([p, c.proffset.to_bytes(1, bo, signed=False)])      # 1 byte
    p = eb.join([p, c.poffset.to_bytes(1, bo, signed=True)])        # 1 byte
    p = eb.join([p, c.instrument.to_bytes(1, bo, signed=False)])    # 1 byte
    for n in c.notes:                                               # 128 bytes (64*2)
        p = eb.join([p, NoteFromClass(n)])
    return p

def ProjectVerify(d: bytes):
    if d[:8] != SIG.encode():
        raise InvalidSignature
    v = int.from_bytes(d[8:10], bo, signed=False)
    if v < VERSION:
        print(v)
        raise ProjectTooOld
    if v > VERSION:
        print(v)
        raise ProjectTooNew
    # TODO: ADD CHECK FOR ":3" ENDING

def ProjectToClass(d: bytes, force=False):
    if not force: # if you use force, it skips all checks and try to convert in anyway
        ProjectVerify(d[:10])
    ic = iToI(d[209], False, 1)
    pc = iToI(d[210], False, 1)
    proj = hd.TrProject(pc, d[12:140].decode()[:d[12:140].decode().index(sp)]) # name as sp terminated string, because sp was used for paddings
    proj.ecn = ECN # d[10:12].decode()
    proj.instruments = []
    proj.author = d[140:204].decode()[:d[140:204].decode().index(sp)] # also sp terminated string
    proj.time = int().from_bytes(d[204:206], bo, signed=False)
    proj.rootnote = iToI(d[206], True, 1)
    proj.tempo = int().from_bytes(d[207:209], bo, signed=True)
    d = d[211:]
    for i in range(ic):
        proj.instruments.append(InstrumentToClass(d[:256]))
        d = d[256:]
    for i in range(pc):
        proj.patterns[i] = PatternToClass(d[:134])
        d = d[134:]
    return proj

def ProjectFromClass(c: hd.TrProject):
    f = bytes()
    f = eb.join([f, SIG.encode()])                                      # 8 bytes SIG
    f = eb.join([f, VERSION.to_bytes(2, bo, signed=False)])             # 2 bytes
    f = eb.join([f, ECN.encode()])                                      # 2 bytes ECN
    f = eb.join([f, pr(c.name, 128, sp).encode()])                      # 128 bytes
    f = eb.join([f, pr(c.author, 64, sp).encode()])                     # 64 bytes
    f = eb.join([f, c.time.to_bytes(2, bo, signed=False)])              # 2 bytes
    f = eb.join([f, c.rootnote.to_bytes(1, bo, signed=True)])           # 1 byte
    f = eb.join([f, c.tempo.to_bytes(2, bo, signed=True)])              # 2 bytes
    f = eb.join([f, len(c.instruments).to_bytes(1, bo, signed=False)])  # 1 byte
    f = eb.join([f, len(c.patterns).to_bytes(1, bo, signed=False)])     # 1 byte
    for i in c.instruments:                                             # ins*256 bytes
        f = eb.join([f, InstrumentFromClass(i)])
    for p in c.patterns:                                                # pat*134 bytes
        f = eb.join([f, PatternFromClass(p)])
    f = eb.join([f, (":3"*32).encode()])                               # 64 bytes
    return f

########################################################################################
def saveProj(path, proj):
    open(path, 'wb').write(ProjectFromClass(proj))

def readProj(path, force=False):
    return ProjectToClass(open(path, 'rb').read(), force=force)

########################################################################################
# encoding config
bo = "big"                  # byteorder, change if needed, not sure what cpp will use
sp = "\x00"                 # for paddings, should be "\x00", because it will also work as string terminator
eb = bytes()                # empty bytes, im almost sure this is needed. used for concatenating bytes
VERSION = 5                 # version of this file format, keep it same as in cf/xetrproj.h
DEBUGCHR = "A"              # in .decode() will raise Error, char will be replaced with that instead crashing whole program
SIG = "XeTrProj"            # dont change
ECN = "PY"                  # should be PY because this encoder is made in py

if __name__ == "__main__":
    # that was to test stuff
    insc, patc, name, tempo = 1, 4, "__NAME__", 120
    file = hd.TrProject(patc, name, tempo, instc)
    f = ProjectFromClass(file)
    el = 8+2+128+64+2+1+2+1+1+(insc*256)+(patc*(134)) + 64
    if len(f) == el:
        for ch in f:
            try:
                cr = ch.to_bytes(1, bo, signed=False).decode()
            except UnicodeDecodeError:
                cr = DEBUGCHR
            sys.stdout.write(cr)
        sys.stdout.flush
    else:
        print(f"wrong len, it should be {el}, but its {len(f)}")
        print(f)
