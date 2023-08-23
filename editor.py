#!/usr/bin/python3
import fg as gen
import hd
import tx
import pickle
from random import random
import chords

def sv():
    if cproj is None or saved:
        return
    try:
        while True:
            match input("save? [Y/n]").lower():
                case "y":
                    cproj.save(fileloc)
                    break
                case "n":
                    break
                case _:
                    pass
    except EOFError:
        print("not saved, because EOF")

def ahf(cr=None): # AUTO HRF
    if cproj is not None:
        print(hd.hrf(cproj, a=av, current=cr))

def exc(g: list):
    global cb
    global fileloc
    global cproj
    global saved
    global pi
    global i
    cmd = g.pop(0)                              # pop command form list, making g args and cmd real command
    if cmd[0] == ".":                           # if you use "." before command, it will try to match it even if its not in tx.cmds, use it for dev commands
        cmd = cmd[1:]
    else:
        if not tx.cmds.__contains__(cmd):
            print(tx.IC)
            return
    match cmd:
        case "help":
                    if len(g) > 0:
                        print(tx.USAGE, f"{hd.color_command}{g[0]}{hd.color_reset} {tx.cmds[g[0]][1]}")
                        return
                    print("remember to use '/' prefix before every command")
                    for nm in tx.cmds.keys():
                        print(f"{hd.color_command}{nm}{hd.color_reset}", "-", tx.cmds[nm][0])
        case "exit":                           # exit
            raise KeyboardInterrupt            #   it just jump to except in main which handle exiting
        case "new":                            # create new file
            sv()
            fileloc = g[0] + ".xetrp"
            cproj = gen.empty(4, g[0])
            cb = tx.ENAME + cproj.name
       	    saved = False
        case "random":
            sv()
            fileloc = g[0] + ".xetrp"
            cproj = gen.random(4, g[0])
            cb = tx.ENAME + cproj.name
       	    saved = False
        case "load":                           # load file from disk
            sv()
            try:
                fileloc = g[0]
                f = open(fileloc, "rb")
                cproj = pickle.load(f)
                f.close()
                cb = tx.ENAME + cproj.name
                saved = True
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
        case "go":
            pi, i = int(g[0]), int(g[1])
        case "save":                           # save current file
            cproj.save(fileloc)
            saved = True
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
                saved = False
            except IndexError:
                print(cproj.rootnote)
        case "len":                            # set len of pattern play range
            if len(g) == 0:
                print(cproj.getLen(pi))
                return
            if cproj.setLen(pi, int(g[0])):
                saved = False
                return
            print(tx.POOR, "or given len is too big or too small")
        case "ofs":
            if cproj.setPROffset(pi, int(g[0])):
                saved = False
                return
            print(tx.POOR)
        case "plo":                            # when in play range first note will be
            if cproj.setPOffset(pi, int(g[0])):
                saved = False
                return
            print(tx.POOR)
        case "shf":                            # shift every value in pattern by g[1]
            cproj.shift(pi, int(g[0]))
        case "cpv":                            # COPY VALUES FROM PATTERN WITH ID PI TO PATTERN WITH ID PA
            for ni in range(hd.MPL):
                cproj.patterns[int(g[0])].values[ni] = cproj.patterns[pi].values[ni]
            saved = False
        case "mute":
            cproj.mute(pi)
            saved = False
        case "unmute":
            cproj.unmute(pi)
            saved = False
        case "lock":
            cproj.lock(pi)
            saved = False
        case "unlock":
            cproj.unlock(pi)
            saved = False
        case "ap":
            cproj.patterns.append(hd.TrPattern())
            saved = False
        case "rp":
            if cproj.patterns[pi].locked:
                raise hd.locked
            cproj.patterns.pop(pi)
            pi = (pi-1)%len(cproj.patterns)
            saved = False
        case "reload":                          # make this like end current editor process, and start new in which will be loaded current project from file
            if not tx.areYouSure():
                return
            f = open(fileloc, "rb")
            cproj = pickle.load(f)
            f.close()
            cb = tx.ENAME + cproj.name
            pi, i = 0, 0
            saved = True
        case "chrd":
            n = cproj.read(pi, i)
            chr = chords.mch(str(g[0]))
            if len(chr) > len(cproj.patterns):
                raise chords.nmp
            for ni in range(len(chr)):
                cproj.write((pi + ni) % len(cproj.patterns), i, chr[ni] + n)
            saved = False
        # NOT READY FUNCTIONS, DEV ONLY
        case "ldt":                             # load patterns from file to cproj
            sv()
            try:
                cproj.patterns = pickle.load(open(g[0], "rb")).patterns
                saved = False
            except IndexError:
                print("index err")

print(f"{hd.color_reset}\nwelcome to XeTracker!\nuse {hd.color_command}/help{hd.color_reset} for help\n")

av = False # use values
am = False
saved = True
cb = tx.ENAME
fileloc = ""
cproj = None
pi = 0
i = 0

try:
    while True:
        ahf(cr=[pi, i])
        cm = input("\n" + cb + ("*"*(not saved)) + " # ")
        cm = hd.cleanS(cm)
        cm += "p"*(cm == "") # if cm is empty then set it to "+0"
        try:
            match cm[0]:
                case "p": # pass
                    pass
                case "q": # quit
                    raise KeyboardInterrupt
                case "/":
                    exc(cm[1:].split(" "))
                case "%":
                    print("debug")
                    match cm[1:]:
                        case "hv":
                            av = not av
                            print("av is now using:", av*"hrf"+(not av)*"values")
                        case "am":
                            am = not am
                            print("auto move is now", am*"enabled"+(not am)*"disabled")
                case _:
                    if cproj is not None:
                        if cm.isdecimal():
                            cproj.write(pi, i, int(cm))
                            saved = False
                            i += am
                        if cm[0] == "+":
                            cproj.write(pi, i, cproj.read(pi, i) + int(cm[1:]))
                            saved = False
                            i += am
                        if cm[0] == "-":
                            cproj.write(pi, i, cproj.read(pi, i) - int(cm[1:]))
                            saved = False
                            i += am
                        match cm:
                            case "l": # move to left
                                pi = (pi-1)%len(cproj.patterns)
                            case "r": # move to right
                                pi = (pi+1)%len(cproj.patterns)
                            case "u": # move up
                                i = (i-1)%hd.MPL
                            case "d": # move down
                                i = (i+1)%hd.MPL
                            case "s": # save
                                cproj.save(fileloc)
                                saved = True
        except hd.locked:
            print(tx.LK)
        except chords.chrdnf:
            print(tx.CHRDNF)
        except chords.nmp:
            print(tx.NPM)
        except IndexError:
            print(tx.IU)
        except AttributeError:
            print(tx.OD)
        except KeyboardInterrupt: # because else instead quiting it would print "something went wrong..."
            raise KeyboardInterrupt
        except:
            print("something went wrong, and it wasnt caught by other exceptions, you may want to restart XeTracker now")
except KeyboardInterrupt:
    print("\n")
    sv()
