#!/usr/bin/python3

fn = [
"clean.sh",
"editor.py",
"fg.py",
"hd.py",
"tx.py",
"readme.md",
"chords.py",
"cf.py",
"src/build_player.sh",
"src/player.cpp",
"src/cf_visualize.py",
"src/xetrproj.hpp",
"src/p2f.hpp",
"changelog.md",
"docs/files.md",
"docs/xetrproj file.md",
"docs/xetrproj.hpp exit codes.md"
]


tch = 0
tl = 0
for nm in fn:
    d = open(nm, "r").read()
    tch += len(d)
    tl += len(d.split("\n"))

print("total lines:", tl)
print("total characters:", tch)
