# this file just have all config and definitions for editor and player

import pickle
MPL = 64                                                # changing this will break everything when loading old project
HRFLW = 8                                               # TODO: THIS SHOULD DEPEND ON NUMBER OF PATTERNS IN PROJECT

leghrf = False                                          # TODO: ADD CHECK IF PRINT OUTPUT SUPPORT COLORS AND SET IT THEN
color_reset, color_invert, color_index, color_first, color_current, color_locked, color_muted, color_command = "", "", "", "", "", "", "", ""
if not leghrf:
    color_reset = "\033[0m"                             # reset everything
    color_invert = "\033[7m"                            # invert bacground and text color
    color_index = color_reset + "\033[36m"              # color of index
    color_first = color_invert + "\033[46m"             # color of first not in playrange
    color_current = "\033[1m"                           # now its used!
    color_locked = "\033[41m"                           # when locked
    color_muted = "\033[41m\033[30m"                    # when pattern is muted
    color_command = "\033[46m"                          # highlight commands

# ----EXCEPTIONS----
class locked(Exception):
    """when trying to edit locked pattern"""
    pass

# ------CLASSS------
class TrPattern:
    def __init__(self, l=8, ofs=0, pofs=0):
        self.values = []
        self.prlen = l          # length of play range
        self.proffset = ofs     # where play range starts
        self.poffset = pofs     # where in play range, first note is (for player)
        self.locked = False
        self.muted = False
        for i in range(MPL):
            self.values.append(0)

    def read(self, i):
        return self.values[i]

    def write(self, i, val):
        if self.locked:
            raise locked
        self.values[i] = val

    def isInPR(self, i):
        start = self.proffset % MPL
        end = (self.prlen + self.proffset) % MPL
        return (start == end) or ((start < end) and (i >= start) and (i < end)) or ((end < start) and ((i >= 0 and i < end) or (i <= MPL and i >= start)))

    def fPVI(self): # first player value index
        return (self.proffset + ((self.poffset)%self.prlen)) % MPL


class TrFile:
    def __init__(self, pcount: int, name: str, tempo=120):
        self.patterns = []
        self.name = name
        self.tempo = tempo
        self.rootnote = 3       # its c, set to 0 for a
        for i in range(pcount):
            self.patterns.append(TrPattern())

    def save(self, path):
        f = open(path, 'wb')
        pickle.dump(self, f)
        f.close()

    def getLen(self, pi: int):
        return self.patterns[pi].prlen

    def setLen(self, pi: int, l:int):
        try:
            if (l > 64 or l < 1):
                return False
            self.patterns[pi].prlen = l
            self.patterns[pi].poffset = self.patterns[pi].poffset % self.patterns[pi].prlen
        except IndexError:
            return False
        return True

    def getTempo(self):
        return self.tempo

    def setTempo(self, t: int):
        self.tempo = t

    def read(self, pi, i):
        return self.patterns[pi].read(i)

    def write(self, pi, i, val):
        return self.patterns[pi].write(i, val)

    def playerRead(self, pi, i):
        cp = self.patterns[pi]
        return self.rootnote + cp.read((cp.proffset + ((i+cp.poffset)%cp.prlen)) % MPL)

    def setPROffset(self, pi: int, o: int):
        try:
            self.patterns[pi].proffset = o % MPL
        except IndexError:
            return False
        return True

    def getPROffset(self, pi: int):
        return self.patterns[pi].proffset

    def setPOffset(self, pi: int, val: int):
        try:
            self.patterns[pi].poffset = val % self.patterns[pi].prlen
        except IndexError:
            return False
        return True

    def getPOffset(self, pi: int):
        return self.patterns[pi].poffset

    def isInPR(self, pi: int, i: int):
        return self.patterns[pi].isInPR(i)

    def isInPRAll(self, i: int):
        # test for every pattern and check if i it's in patterns PR if so, return True if for every pattern its outside PR it will be Fale
        m = False
        for pt in self.patterns:
            m = m or (pt.isInPR(i) and not pt.muted)
        return m

    def setRN(self, n: int):
        self.rootnote = n

    def lock(self, pi: int):
        self.patterns[pi].locked = True

    def unlock(self, pi: int):
        self.patterns[pi].locked = False

    def mute(self, pi: int):
        self.patterns[pi].muted = True

    def unmute(self, pi: int):
        self.patterns[pi].muted = False

    def shift(self, pi: int, val: int):
        for i in range(MPL):
            self.patterns[pi].write(i, self.patterns[pi].read(i) + val)

def padstr(s: str, l: int):
    if len(s) > l:
        return "#" * l
    return s + (l-len(s)) * " "

def hrf(pr: TrFile, a=True, h=True, current=None):
    g = ""
    if h:   # HEADER
        g = g + padstr("", HRFLW) + " "
        for i in range(len(pr.patterns)):
            g = g + color_index + padstr(str(hex(i))[2:] + color_reset, HRFLW+len(color_reset))
        g = g + "\n"
    for i in range(MPL):
        if a or pr.isInPRAll(i):
            g = g + color_index + padstr(str(hex(i))[2:], HRFLW) + color_reset + " "
            for pi in range(len(pr.patterns)):
                pt = pr.patterns[pi]
                if current is not None and pi == current[0] and i == current[1]:
                    g = g + color_current + padstr(str(hex(pt.read(i)))[2:] + color_reset, HRFLW+len(color_reset))
                elif pt.muted:                      # muted pattern
                    g = g + color_muted + padstr(str(hex(pt.read(i)))[2:] + color_reset, HRFLW+len(color_reset))
                elif i == pt.fPVI():                # first play range note (first played by player i mean)
                    g = g + color_first + padstr(str(hex(pt.read(i)))[2:] + color_reset, HRFLW+len(color_reset))
                elif pt.locked and pt.isInPR(i):    # play range of locked pattern
                    g = g + color_invert + color_locked + padstr(str(hex(pt.read(i)))[2:] + color_reset, HRFLW+len(color_reset))
                elif pt.locked:                     # locked pattern
                    g = g + color_locked + padstr(str(hex(pt.read(i)))[2:] + color_reset, HRFLW+len(color_reset))
                elif pt.isInPR(i):                  # play ranges
                    g = g + color_invert + padstr(str(hex(pt.read(i)))[2:] + color_reset, HRFLW+len(color_reset))
                else:                               # just print it as normal text
                    g = g + padstr(str(hex(pt.read(i)))[2:], HRFLW)
            g = g + "\n"
    return "\r" + g + color_reset + "\n"

def cleanS(s: str):
    try:
        while s[0] == " ":
            s = s[1:]
        while s[-1] == " ":
            s = s[:-1]
        return s
    except IndexError:
        return ""
