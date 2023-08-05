#!/usr/bin/python3

fn = [
"clean.sh",
"dev.sh",
"editor.py",
"fg.py",
"hd.py",
"p2f.py",
"player.py",
"test.sh",
"readme.md"]

tch = 0
tl = 0
for nm in fn:
    d = open(nm, "r").read()
    tch += len(d)
    tl += len(d.split("\n"))

print("total lines:", tl)
print("total characters:", tch)
