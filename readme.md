# welcome
this is XeTracker project<br>
probably only tracker software made to work in tty mode<br>

# setup
execute this command to build and set permissions for all things<br>
`echo -e "setting up!\n"; chmod +x editor.py clean.sh count.py cf.py src/build_player.sh src/cf_visualize.py; cd src; ./build_player.sh; cd ..`

# usage
## move cursor
`u` - move up<br>
`d` - move down<br>
`r` - more right<br>
`l` - more left<br>

## prefixes
None - set value in place where you are<br>
`+` - add to value in place where you are<br>
`/` - execute command<br>
`%` - set config<br>

## other one character inputs
`p` - do nothing, idk why its even here<br>
`q` - quit<br>
`s` - save<br>

# config
`hv` - set it to display all patterns in project or only ranges of patterns that will be played by player<br>
`am` - if its enabled, cursor will move after every change of value (after every input with no prefix or with `+` or `-` prefix)<br>

# other
list commands by executing `/help` in editor<br>
if you test dev commands (that arent listed in tx.cmds) you need to put "." before command<br>

# playing
to play you need player and soundgen: `./player.py [your projectname].xetrp | src/soundgen`<br>
player is to read data from project file and output as text<br>
soundgen is to get from this text info like volume and frequency, and convert it to real sound<br>
