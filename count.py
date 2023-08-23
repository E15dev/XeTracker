#!/usr/bin/python3

fn = [
"clean.sh",
"editor.py",
"fg.py",
"hd.py",
"tx.py",
"p2f.py",
"player.py",
"readme.md",
"sg/build.sh",
"sg/soundgen.cpp",
"sg/sg.h",
"sg/rand.py",
"chords.py"]

tch = 0
tl = 0
for nm in fn:
    d = open(nm, "r").read()
    tch += len(d)
    tl += len(d.split("\n"))

print("total lines:", tl)
print("total characters:", tch)
