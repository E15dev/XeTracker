#!/usr/bin/python3
import fg as gen
import hd
import tx
from random import random
import chords
from time import time
from cf import saveProj, readProj

def sv():
    if cproj is None or saved: return
    cproj.time += round(time() - timeS)
    timeS = time()
    try:
        while True:
            match input("save? [Y/n]").lower():
                case "y":
                    saveProj(fileloc, cproj)
                    break
                case "n":
                    break
                case _:
                    pass
    except EOFError:
        print("not saved, because EOF")

def ahf(cr=None):
    if cproj is not None and len(cproj.patterns) > 0:
        print(hd.hrf(cproj, a=av, current=cr))

def exc(g: list):
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
            fileloc = g[0] + ".xetrproj"
            cproj = gen.empty(4, g[0])
       	    saved = False
        case "random":
            sv()
            fileloc = g[0] + ".xetrproj"
            cproj = gen.random(4, g[0])
       	    saved = False
        case "load":                           # load file from disk
            sv()
            try:
                fileloc = g[0]
                cproj = readProj(fileloc)
                saved = True
            except FileNotFoundError:
                print("file not found")
        case "unload":
            sv()
            cproj = None
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
            saveProj(fileloc, cproj)
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
        case "cpv":                            # COPY NOTES FROM PATTERN WITH ID PI TO PATTERN WITH ID PA
            for ni in range(hd.MPL):
                cproj.patterns[int(g[0])].notes[ni] = cproj.patterns[pi].notes[ni]
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
            pi = (pi-1)%(len(cproj.patterns) + (len(cproj.patterns)<1)) # so wont be 0DivErr when you delete last pattern. also after deleting last pattern pi will be always be set to 0 which is not breaking anything
            saved = False
        case "reload":                          # make this like end current editor process, and start new in which will be loaded current project from file
            if not tx.areYouSure():
                return
            cproj = readProj(fileloc)
            pi, i = 0, 0
            saved = True
        case "chrd":
            n = cproj.read(pi, i).pitch
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
                cproj.patterns = readProj(g[0]).patterns
                saved = False
            except IndexError:
                print("index err")
        case "time":
            print(cproj.time + round(time()-timeS))
        case "name":
            tmp = ""
            for s in g: # beause args are space separated, it need to connect them back to have spaces
                tmp = tmp + " " + s
            cproj.name = s
        case "sine": # set instrument of selected pattern to sine
            cproj.instruments.append(gen.instrumentSine())
            cproj.patterns[pi].instrument = len(cproj.instruments)-1
            saved = False
            print(cproj.instruments)


print(f"{hd.color_reset}\nwelcome to XeTracker!\nuse {hd.color_command}/help{hd.color_reset} for help\n")

av = False # use values
am = False
saved = True
fileloc = ""
cproj = None
pi = 0
i = 0
timeS = time()

try:
    while True:
        ahf(cr=[pi, i])
        cm = input("\n" + tx.ENAME + (cproj.name if cproj is not None else "") + ("*"*(not saved)) + "# ")
        cm = hd.cleanS(cm)
        cm += "p"*(cm == "") # if cm is empty then set it to "+0", which means it wont change anything, but will triger auto move
        try:
            match cm[0]:
                case "p": # pass
                    pass
                case "q": # quit
                    raise KeyboardInterrupt
                case "/":
                    exc(cm[1:].split(" "))
                case "%":
                    match cm[1:]:
                        case "hv":
                            av = not av
                            print("av is now using:", "hrf" if av else "values")
                        case "am":
                            am = not am
                            print("auto move is now", "enabled" if am else "disabled")
                case _: # now these things which needs cproj to not be None
                    vf = True
                    if cproj is not None:
                        if cm[0] == "v":
                            vf = False
                            cm = cm[1:]
                        if cm.isdecimal():
                            cproj.write(pi, i, pitch=int(cm)) if vf else cproj.write(pi, i, vol=int(cm))
                            saved = False
                            i += am
                        if cm[0] == "+":
                            cproj.write(pi, i, pitch=cproj.read(pi, i).pitch + int(cm[1:])) if vf else cproj.write(pi, i, vol=cproj.read(pi, i).vol + int(cm[1:]))
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
                                cproj.time += round(time()-timeS)
                                timeS = time()
                                saveProj(fileloc, cproj)
                                saved = True
        except hd.locked:
            print(tx.LK)
        except chords.chrdnf:
            print(tx.CHRDNF)
        except chords.nmp:
            print(tx.NPM)
        except IndexError:
            print(tx.IU)
#        except AttributeError:
#            print(tx.OD)
        except KeyboardInterrupt: # because else instead quiting it would print "something went wrong..."
            raise KeyboardInterrupt
#        except:
#            print("something went wrong, and it wasnt caught by other exceptions, you may want to restart XeTracker now")
except KeyboardInterrupt:
    print("\n")
    sv()
