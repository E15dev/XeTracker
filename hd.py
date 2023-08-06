# this file just have all config and definitions for editor and player


import pickle
MPL = 64                                                # changing this will break everything when loading old project


COMMANDS = """
help            - prints this help
exit            - exit editor
auto            - enable/disable hrf after every command
hv              - subsetting for "auto" command, set if use hrf or values
new NAME        - crate project NAME
save            - save project as "{CPROJ.NAME}.xetrp"
load PATH       - load project from given PATH
hrf             - show all values in all patterns
values          - like hrf but skip all places outside playranges
set PI I VAL    - set value I in pattern PI to VAL
tempo [TEMPO]   - set project tempo to TEMPO or show current tempo if no args
len PI VAL      - set play range len of patter PI to VAL
ofs PI VAL      - set play range offset of pattern PI to VAL
plo PI VAL      - set which note is first in play range
"""


ENAME = "XeTrEditor:"                                   # base comman input (no project name)
NPY = "you arent editing any project yet"               # error message when you dont have loaded project
POOR = "probably pattern id is too big"                 # error when trying to access pattern out of range
leghrf = False                                          # TODO: ADD CHECK IF PRINT OUTPUT SUPPORT COLORS AND SET IT THEN
color_reset, color_invert, color_index, color_first, color_current = "", "", "", "", ""
if not leghrf:
    color_reset = "\033[0m"                             # reset everything
    color_invert = "\033[7m"                            # invert bacground and text color
    color_index = "\033[36m"                            # color of index
    color_first = color_invert + "\033[46m"             # color of first not in playrange
    color_current = "\033[1m"                           # CURRENT IS NOT USED YET, WILL BE WHEN I WILL MADE BETTER EDITOR SO YOU COULD LIKE USE ARROWS TO SELECT WHICH TO MODIFY AND NOT NEED TO USE (hrf) and (set) EVERY TIME

# class TrVal:
#     def __init(self, pitch, volume):
#         self.pitch = pitch
#         self.volume = volume            # x00 to xff pls
#         self.m0 = 0
#         self.m1 = 0
#         self.m2 = 0
#         self.m3 = 0
#         # TODO: MAYBE USE THIS LATER, NOW ITS EXPERIMENTAL
#         # TODO: AUTOMATIONS, LIKE THAT ILL BE INTERPOLATED BY PLAYER, BUT I GUESS STORE IT IN PATTERN NOT IN THIS

class TrPattern:
    def __init__(self, l=8, ofs=0, pofs=0):
        self.values = []
        self.prlen = l          # length of play range
        self.proffset = ofs     # where play range starts
        self.poffset = pofs     # where in play range, first note is (for player)
        for i in range(MPL):
            self.values.append(0)

    def read(self, i):
        return self.values[i]

    def write(self, i, val):
        self.values[i] = val

    def isInPR(self, i):
        start = self.proffset % MPL
        end = (self.prlen + self.proffset) % MPL
        return ((start < end) and (i >= start) and (i < end)) or ((end < start) and ((i >= 0 and i < end) or (i <= MPL and i >= start)))

    def fPVI(self): # first player value index
        return (self.proffset + ((self.poffset)%self.prlen)) % MPL


class TrFile:
    def __init__(self, pcount: int, name: str, tempo=120):
        self.patterns = []
        self.name = name
        self.tempo = tempo
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
        return cp.read((cp.proffset + ((i+cp.poffset)%cp.prlen)) % MPL)

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
            m = m or pt.isInPR(i)
        return m


def padstr(s: str, l: int):
    if len(s) > l:
        return "#" * l
    return s + (l-len(s)) * " "

def hrf(pr: TrFile, a=True):
    g = ""
    for i in range(MPL):
        if a or pr.isInPRAll(i):
            g = g + color_index + padstr(str(hex(i))[2:], 6) + color_reset + " "
            for pt in pr.patterns:
                if i == pt.fPVI():
                    g = g + color_first + padstr(str(hex(pt.read(i)))[2:] + color_reset, 6+len(color_reset))
                elif pt.isInPR(i):
                    g = g + color_invert + padstr(str(hex(pt.read(i)))[2:] + color_reset, 6+len(color_reset))
                else:
                    g = g + padstr(str(hex(pt.read(i)))[2:], 6)
            g = g + "\n"
    return "\r" + g + color_reset + "\n"
