# welcome
this is XeTracker project<br>
probably only tracker software made to work in tty mode<br>

# setup
execute this command to build and set permissions for all things~~, would be easier if i knew how to use makefiles~~
`echo -e "setting up!\n"; chmod +x editor.py p2f.py player.py clean.sh count.py src/build_sg.sh src/rand.py cf.py src/build_cf.sh; cd src; ./build_sg.sh; ./build_cf.sh; cd ..`

# usage
## move cursor
`u` - move up</br>
`d` - move down</br>
`r` - more right</br>
`l` - more left</br>

## prefixes
None - set value in place where you are</br>
`+` - add to value in place where you are</br>
`-` - substract from value in place where you are</br>
`/` - execute command</br>
`%` - set config</br>

## other one character inputs
`p` - do nothing, idk why its even here</br>
`q` - quit</br>
`s` - save</br>

# config
`hv` - set it to display all patterns in project or only ranges of patterns that will be played by player</br>
`am` - if its enabled, cursor will move after every change of value (after every input with no prefix or with `+` or `-` prefix)</br>

# other
list commands by executing `/help` in editor<br>
if you test dev commands (that arent listed in tx.cmds) you need to put "." before command<br>

<!--DO THAT BACK LATER, I MEAN COMMAND CHAINS IN EDITOR-->
<!--you can also use `;` between command and it will be like list of commands, for example `new test;set 1 1 1;hrf;save;exit`<br>-->
<!--# usage example-->
<!--1. with editor create example project: `echo -e "new test; tempo 113; set 0 1 12; set 0 3 24; set 0 4 12; set 0 6 7; mute 3; mute 2; mute 1; save; exit" | ./editor.py`-->

# playing
to play you need player and soundgen: `./player.py [your projectname].xetrp | src/soundgen`</br>
player is to read data from project file and output as text</br>
soundgen is to get from this text info like volume and frequency, and convert it to real sound</br>
