#!/usr/bin/python3
import fg as gen
import hd
import pickle

print("\nwelcome to XeTracker!\nuse help for help\n")

ah = False
av = True
saved = True

def sv():
    if cproj is None or saved:
        return
    while True:
        ic = input("save? [Y/n]")[0].lower()
        if ic == "y":
            cproj.save(fileloc)
            break
        if ic == "n":
            break

def ahf(): # AUTO HRF
    global ah
    if cproj is not None and ah:
        print(hd.hrf(cproj, a=av))

def exc(g: list):
    global cb
    global fileloc
    global cproj
    global ah
    global av
    global saved
    cmd = g.pop(0)                              # pop command form list making g args and cmd real command
    if cmd == "help":
        print(hd.COMMANDS)
        return
    if cmd == "exit":                           # exit
        raise KeyboardInterrupt                 #   it just jump to except in main which handle exiting correctly
    if cmd == "auto":                           # enable/disable auto printing after every command
        ah = not ah
        print("auto hrf is now set to:", ah)
        return
    if cmd == "hv":                             # in ahf, use like values or default hrf
        av = not av
        print("auto hrf is now using:", av*"hrf"+(not av)*"values") # who would ever use if...
        return
    if cmd == "new":                            # create new file
        sv()
        fileloc = g[0] + ".xetrp"
        cproj = gen.empty(4, g[0])
        cb = hd.ENAME + cproj.name
       	saved = False
        ahf()
        return
    if cmd == "random":
        sv()
        fileloc = g[0] + ".xetrp"
        cproj = gen.random(4, g[0])
        cb = hd.ENAME + cproj.name
       	saved = False
        ahf()
        return
    if cmd == "save":                           # save current file
        if cproj is not None:
            cproj.save(fileloc)
       	    saved = True
            return
        print(hd.NPY)
        return
    if cmd == "load":                           # load file from disk
        sv()
        try:
            fileloc = g[0]
            f = open(fileloc, "rb")
            cproj = pickle.load(f)
            f.close()
            cb = hd.ENAME + cproj.name
            saved = True
            ahf()
        except FileNotFoundError:
            print("file not found")
        return
    if cmd == "hrf":                            # print all values in all patterns in human readable fomat
        if cproj is not None:
            print(hd.hrf(cproj))
            return
        print(hd.NPY)
        return
    if cmd == "values":                         # like hrf but stop printing after last play range end
        if cproj is not None:
            print(hd.hrf(cproj, a=False))
            return
        print(hd.NPY)
        return
    if cmd == "set":                            # set value
        if cproj is None:
            print(hd.NPY)
            return
        try:
            if len(g) < 3:
                raise IndexError
            cproj.write(int(g[0]), int(g[1]), int(g[2]))
            saved = False
            ahf()
            return
        except IndexError:
            print("usage: set PATTERN INDEX VALUE")
            return
        except ValueError:
            print("usage: set PATTERN INDEX VALUE")
            return
    if cmd == "tempo":                          # set or get tempo
        if cproj is None:
            print(hd.NPY)
            return
        try:
            cproj.setTempo(int(g[0]))
            saved = False
        except IndexError:
            print(cproj.getTempo())
        return
    if cmd == "len":                            # set len of pattern play range
        if cproj is None:
            print(hd.NPY)
            return
        cproj.setLen(int(g[0]), int(g[1]))
        saved = False
        ahf()
        return
    if cmd == "ofs":
        if cproj is None:
            print(hd.NPY)
            return
        cproj.setPROffset(int(g[0]), int(g[1]))
        saved = False
        ahf()
        return
    if cmd == "plo":                            # when in play range first note will be
        if cproj is None:
            print(hd.NPY)
            return
        cproj.setPOffset(int(g[0]), int(g[1]))
        saved = False
        ahf()
        return
    if cmd == "ldt":                            # THIS IS DEV ONLY FUNCTION, SHOULDNT BE REALLY USED. MAY BREAK A LOT OF THINGS. LOAD PATTERNS FROM ONE FILE TO SECOND
        if cproj is None:
            print(hd.NPY)
            return
        sv()
        try:
            cproj.patterns = pickle.load(open(g[0], "rb")).patterns
            saved = False
            ahf()
        except IndexError:
            print("index err")
        return
    print("invalid command")

cb = hd.ENAME
fileloc = ""
cproj = None
try:
    while True:
        print(cb, end="# ")
        v = input().split(";")
        for cm in v:
            exc(cm.split(" "))
except KeyboardInterrupt:
    print("\n")
    sv()
