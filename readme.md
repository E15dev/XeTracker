# welcome
this is XeTracker project<br>
probably only tracker software made to work in linux tty mode<br>

# setup
you need to install sfml library<br>
all permissions should be set up already, to build player, first cd in to src and then use `./build_player.sh`<br>

# usage
## move cursor
`u` - move up<br>
`d` - move down<br>
`r` - more right<br>
`l` - more left<br>

## prefixes
None - set value in place where you are<br>
`+` - add to value in place where you are (you can do +- to subtract)<br>
`/` - execute command<br>
`%` - set config<br>
`v` - change volume of note, for example `v0` set volume to 0<br>

## other one character inputs
`p` - do nothing, idk why its even here<br>
`q` - quit<br>
`s` - save<br>

# config
`hv` - set it to display all patterns in project or only ranges of patterns that will be played by player<br>
`am` - if its enabled, cursor will move after every change of value (after every input with no prefix or with `+` prefix)<br>

# other
list commands by executing `/help` in editor<br>
if you test dev commands (that aren't listed in tx.cmds) you need to put "." before command name<br>

# playing
to play project you made you just need to use player from src, `src/player [projectname].xetrproj`<br>
