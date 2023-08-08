# welcome
this is XeTracker project<br>
probably only tracker software made to work in tty mode<br>

# setup
`echo -e "setting up!\n"; chmod +x editor.py p2f.py player.py clean.sh count.py sg/build.sh sg/rand.py; cd sg; ./build.sh; cd ..`

# files
`clean.sh` - remove all stuff generated when running + test.xetrp<br>
`count.py` - just to show how many lines and characters i typed<br>
`editor.py` - main program, to edit XeTracker projects<br>
`fg.py` - project generators, like "new" which generate empty file, maybe later i will add project presets for like specific genres<br>
`hd.py` - all important stuff, all classes and definitions<br>
`tx.py` - error messages, info messages, help message<br>
`p2f.py` - converts piped pitch info from player to frequency that will be piped to soundgen<br>
`player.py` - reads singe channel in xetrp files with tempo and pipe it to next program<br>
`readme.md` - this file, you should know this<br>
`sg/build.sh` - to build soundgen<br>
`sg/sg.h` - waves generors<br>
`sg/soundgen.cpp` - sound player<br>
`sg/rand.py` - generate random freq between 220 and 880 hz to test soundgen<br>

# other
list commands by doing `help` in editor<br>
you can also use `;` in commands (no spaces) and it will be like list of commands, for example `new test;set 1 1 1;hrf;save;exit`<br>
if you test dev commands (that arent listed in tx.cmds) you need to put "." before command<br>

# usage example
1. with editor create example project: `echo -e "new test;tempo 113;set 0 1 12;set 0 3 24;set 0 4 12;set 0 6 7;save;exit" | ./editor.py`
2. to play you need few things, player, p2f and soundgen: `./player.py test.xetrp 0 | ./p2f.py | sg/soundgen`
