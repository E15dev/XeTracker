# alpha (06.08.2023)
now you can just use it. works only one channel at the time.

# alpha 2 (also 06.08.2023)
1. lock/unlock patterns
2. mute/unmute patterns
3. command `unload`
4. ability to set root note, and default is now c not a

# alpha 3 (08.08.2023)
1. almost now way to crash editor
2. command `shf`
3. command `cpv`
4. editor use now `match` instead `if`
5. header in `hd.hrf`
6. soundgen doesnt regenerate sound if frequency is same as it was
7. limit on pattern len
8. fixed hrf on pattern len=64
9. variable hd.HRFLW instead number 6 in hd.hrf, that means you will be able to set how much space one pattern take in hrf/values
10. help and info message are now in tx.py instead hd.py
11. usage added for every command
12. checking if command exist before trying to match it, remember to add command to tx.cmds if you are coding new one
13. dev commands are now by default rejected unless you use "." before it
14. using space on end of command dont break everything
15. "remove pattern" and "add pattern" functions (dev only for now)


# beta (23.08.2023)
1. totally new editor, and color_current is being used
2. better save function
3. command can have a lot of spaces on beggining and end and still work
4. clean.sh use -f
5. `rp` and `ap` functions are now official
6. `reload` function (close current project and load it from last save)
7. highlighting commands (in help)
8. if no patterns specified as player.py args, it will play all not muted ones
9. `chrd` command and chords.py file
10. `tx.NMP` - if you need more patterns to do that action

# beta 2
1. docs
2. custom file format
3. cf_visualize.py for debugin custom file format
4. moved stuff to `src` dir

# beta 3 (10.09.2023)
1. renamed `cf.cpp` and `build_cf.sh` to `cfv.cpp` and `build_cfv.sh`
2. rewrite of sg.h
3. file format v5, added encoder name (2 bytes)

# beta 4 (16.09.2023)
1. project class in xetrproj.hpp
2. support of wavetable instrument in sg.h
3. note volume support in editor<!--m,aybe it was already in beta 3, im not sure-->
4. player is now in c++ only
5. dir `/old` for programs that wont be needed anymore
