# xetrproj format:
## file
1. 8 bytes is always "XeTrProj"
2. 2 bytes of editor version (unsigned int)
3. 2 bytes of encoder name ("PY" or "C+")
4. 128 bytes of project name (padded with null bytes)
5. 64 bytes of project author name (padded with null bytes)
6. 2 bytes of "time spent on project" in second (unsigned int) which will be measured by editor (MAY NEED TO BE BIGGER)
7. 1 byte of root note (signed)
8. 2 bytes of tempo (signed int)
9. 1 byte number of instruments that are stored in file (unsigned)
10. 1 byte number of patterns that are stored in file (unsigned)
11. (number of instruments)*256 bytes
12. (number of patterns)*(size of pattern)
13. 64 bytes, repeating ":3", <!-- dont even ask why, im writing this at 2 am-->this is end of "project section"
14. (start of this is data section=0) raw data, that will be pointed by for example instruments, like samples

## pattern
1. 1 byte "is_locked" (bool)
2. 1 byte "is_muted" (bool)
3. 1 byte play range len (unsigned), will be only from 1 to 64 tho
4. 1 byte play range ofset (unsigned), will be only from 0 to 63 tho
5. 1 byte start note index (signed), will be from (1-(play range len)) to ((play range len)-1)
6. 1 byte instrument id (unsigned)
7. 64*note

## note
1. 1 byte volume (unsigned)
2. 1 byte pitch (signed)

## instrument
1. 1 byte type
2. 255 bytes data

if type==0x50 (thats "P"), data will be ignored, and everything using this instrument will have no sound</br>
if type==0x53 (thats "S"), data will be null terminated, null padded path to sample on disc, may start with $samples which will be converted to sample folder set by user</br>
if type==0x56 (thats "V"), I HAVE NO IDEA HOW TO IMPLEMENT IT</br>
if type==0x77 (thats "w"), new wavetable, stored in instrument fully</br>
if type==0x73 (thats "s"), first 8 bytes are ofset from "data section" start. next 4 bytes are int, indicating length of sample.</br>

# reading
you can read data from xetrproj file in python, using functions from `cf.py`</br>
you can debug xetrproj files using `src/cf_visualize.py` which is made to pring these files in hexadecimal, with colors (so you need your terminal to support colors)</br>
