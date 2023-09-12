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
"src/build_sg.sh",
"src/soundgen.cpp",
"src/sg.h",
"src/rand.py",
"chords.py",
"cf.py",
"src/build_cfv.sh",
"src/cfv.cpp",
"src/cf_visualize.py",
"src/xetrproj.hpp",
"src/p2f.hpp",
"changelog.md",
"docs/files.md",
"docs/soundgen input format.md",
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
