# list of all files with descriptions
`clean.sh` - remove all stuff generated when running + test.xetrp<br>
`count.py` - just to show how many lines and characters i typed<br>
`editor.py` - main program, to edit XeTracker projects<br>
`fg.py` - project generators, like "new" which generate empty file, maybe later i will add project presets for like specific genres<br>
`hd.py` - all important stuff, all classes and functions<br>
`tx.py` - error messages, info messages, help message, all other kinds of messages<br>
`p2f.py` - converts pitch info from stdin to frequency, convert funciton is used by player also<br>
`player.py` - reads data from xetrp files with right tempo, and convert it to format that soundgen will understand<br>
`chords` - have chords utils<br>
`readme.md` - this file, you should know this<br>
`src/build_sg.sh` - to build soundgen<br>
`src/sg.h` - things for soundgen, like waveforms<br>
`src/soundgen.cpp` - sound generator<br>
`src/rand.py` - generate n of random freq between 220 and 880 hz to test soundgen<br>
`cf.py` - have functions to decode and encode classes from hd, all stuff releated to custom file format<br>
`src/build_cf.sh` - build cf.cpp<br>
`src/cf_visualize.py` - prints project as hex, but also colors different sections of it. used to debug .xetrproj files<br>
`src/cfv.cpp` - should do same thing but in c++, its for testing xetrproj.h<br>
`src/xetrproj.hpp` - have all functions and things needed to decode .xetrproj files<br>
`src/p2f.hpp` - pitch to frequency but in c++ instead python<br>
