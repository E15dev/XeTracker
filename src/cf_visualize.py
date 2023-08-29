#!/bin/python3
import sys
data = open(sys.argv[1], 'rb').read()

sp = " "
reset = sp + "\033[0m"

#decoded = ""
#for ch in data:
#    try:
#        cr = ch.to_bytes(1, "big").decode()
#    except UnicodeDecodeError:
#        cr = "A"
#    decoded = decoded + cr
insc = data[207]
patc = data[208]

h = ""
h = h + "\033[7m"           + data[:8].hex(sp) + reset # sig
h = h + "\033[7;35m"        + data[8:10].hex(sp) + reset # ver
h = h + "\033[36m"          + data[10:138].hex(sp) + reset # name
h = h + "\033[34m"          + data[138:202].hex(sp) + reset # author
h = h + "\033[42m"          + data[202:204].hex(sp) + reset # time spent
h = h + "\033[41m"          + data[204:205].hex(sp) + reset # root note
h = h + "\033[43m"          + data[205:207].hex(sp) + reset # tempo
h = h + "\033[7;31m"        + data[207:208].hex(sp) + reset # insc
h = h + "\033[7;32m"        + data[208:209].hex(sp) + reset # patc
h = h + "\033[31m"          + data[209:209+(insc*256)].hex(sp) + reset # instruments
h = h + "\033[32m"          + data[209+(insc*256):209+(insc*256)+(patc*134)].hex(sp) + reset # patterns
h = h + "\033[7m"           + data[209+(insc*256)+(patc*134):209+(insc*256)+(patc*134)+64].hex(sp) + reset # end
h = h + "\033[48;5;9;31m"   + data[209+(insc*256)+(patc*134)+64:].hex(sp) # whatever will be here probably shouldnt
# btw i have no idea how this esacpe sequences work, it just make visible red on red background, like why 48 make it red, wasnt 41 for red?
print(h[:-1] + reset) # last char is always space
