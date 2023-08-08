#!/usr/bin/python3
import fg as gen
import hd
import tx
import pickle
from random import random

print("\nwelcome to XeTracker!\nuse help for help\n", hd.color_reset)

ah = False
av = True
saved = True

def sv():
    if cproj is None or saved:
        return
    while True:
        try:
            ic = input("save? [Y/n]")[0].lower()
        except EOFError:
            break
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
    if cmd[0] == ".":                           # if you use "." before command, it will try to match it even if its not in tx.cmds, use it for dev commands
        cmd = cmd[1:]
    else:
        if not tx.cmds.__contains__(cmd):
            print(tx.IC)
            return
    match cmd:
        case "help":
            if len(g) > 0:
                print(tx.USAGE, tx.cmds[g[0]][1])
                return
            print("") # fast way for \n, better than print("\n", end="")
            for nm in tx.cmds.keys():
                print(nm, "-", tx.cmds[nm][0])
            print("")
        case "exit":                           # exit
            raise KeyboardInterrupt            #   it just jump to except in main which handle exiting correctly
        # TODO: make config file that will be loaded on every editor session
        case "auto":                           # enable/disable auto printing after every command
            ah = not ah
            print("auto hrf is now:", ah*"enabled"+(not ah)*"disabled")
        case "hv":                             # in ahf, use like values or default hrf
            av = not av
            print("auto hrf is now using:", av*"hrf"+(not av)*"values") # who would ever use if...
        case "new":                            # create new file
            sv()
            fileloc = g[0] + ".xetrp"
            cproj = gen.empty(4, g[0])
            cb = tx.ENAME + cproj.name
       	    saved = False
            ahf()
        case "random":
            sv()
            fileloc = g[0] + ".xetrp"
            cproj = gen.random(4, g[0])
            cb = tx.ENAME + cproj.name
       	    saved = False
            ahf()
        case "save":                           # save current file
            if cproj is not None:
                cproj.save(fileloc)
       	        saved = True
                return
            print(tx.NPY)
        case "load":                           # load file from disk
            sv()
            try:
                fileloc = g[0]
                f = open(fileloc, "rb")
                cproj = pickle.load(f)
                f.close()
                cb = tx.ENAME + cproj.name
                saved = True
                ahf()
            except FileNotFoundError:
                print("file not found")
        case "unload":
            sv()
            cproj = None
            cb = tx.ENAME
            fileloc = ""
            saved = True

        case _:
            if cproj is None:
                print(tx.NPY)
                return
    # these are commands that need cproj to not be None
    match cmd:
        case "hrf":                            # print all values in all patterns in human readable fomat
            print(hd.hrf(cproj))
        case "values":                         # like hrf but stop printing after last play range end
            print(hd.hrf(cproj, a=False))
        case "tempo":                          # set or get tempo
            try:
                cproj.setTempo(int(g[0]))
                saved = False
            except IndexError:
                print(cproj.getTempo())
        case "rn":
            try:
                cproj.rootnote = int(g[0])
            except IndexError:
                print(cproj.rootnote)
        case "set":                            # set value
            if len(g) < 3:
                raise IndexError
            cproj.write(int(g[0]), int(g[1]), int(g[2]))
            saved = False
            ahf()
        case "len":                            # set len of pattern play range
            if len(g) == 1:
                print(cproj.getLen(int(g[0])))
                return
            if cproj.setLen(int(g[0]), int(g[1])):
                saved = False
                ahf()
                return
            print(tx.POOR, "or given len is too big or too small")
        case "ofs":
            if cproj.setPROffset(int(g[0]), int(g[1])):
                saved = False
                ahf()
                return
            print(tx.POOR)
        case "plo":                            # when in play range first note will be
            if cproj.setPOffset(int(g[0]), int(g[1])):
                saved = False
                ahf()
                return
            print(tx.POOR)
        case "shf":                            # shift every value in pattern by g[1]
            cproj.shift(int(g[0]), int(g[1]))
        case "cpv":                            # COPY VALUES FROM PATTERN WITH ID PI TO PATTERN WITH ID PA
            for i in range(hd.MPL):
                cproj.patterns[int(g[1])].values[i] = cproj.patterns[int(g[0])].values[i]
            saved = False
            ahf()
        case "mute":
            cproj.mute(int(g[0]))
            saved = False
            ahf()
        case "unmute":
            cproj.unmute(int(g[0]))
            saved = False
            ahf()
        case "lock":
            cproj.lock(int(g[0]))
            saved = False
            ahf()
        case "unlock":
            cproj.unlock(int(g[0]))
            saved = False
            ahf()
        # NOT READY FUNCTIONS, DEV ONLY
        case "ldt":                            # LOAD PATTERNS FROM ONE FILE TO SECOND
            sv()
            try:
                cproj.patterns = pickle.load(open(g[0], "rb")).patterns
                saved = False
                ahf()
            except IndexError:

                print("index err")
        case "ap":                              # add pattern
            cproj.patterns.append(hd.TrPattern())
            ahf()
            saved = False
        case "rp":                              # remove pattern
            if not cproj.patterns[int(g[0])].locked:
                cproj.patterns.pop(int(g[0]))
                ahf()
                saved = False
cb = tx.ENAME
fileloc = ""
cproj = None
try:
    while True:
        print(cb, end="# ")
        v = input().split(";")
        for cm in v:
            while cm[-1] == " ":
                cm = cm[:-1]
            try:
                exc(cm.split(" "))
            except hd.locked:
                print(tx.LK)
            except IndexError:
                print(tx.USAGE, tx.cmds[cm.split(" ")[0]][1])
            except AttributeError:
                print(tx.OD)
            except KeyboardInterrupt: # because else instead quiting it would print "something went wrong..."
                raise KeyboardInterrupt
            except:
                print("something went wrong, and it wasnt caught by other exceptions, you may want to restart XeTracker now")
except KeyboardInterrupt:
    print("\n")
    sv()
