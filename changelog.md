# alpha (06.08.2023)
now you can just use it. works only one channel at the time. you can just use it. works only one channel at the time.

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
