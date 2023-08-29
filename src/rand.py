#!/usr/bin/python3
import sys
from random import random
from time import time
from math import floor

try:
    c = int(sys.argv[1])
except IndexError:
    c = 1

tn = 0

try:
    while True:
        while time() - tn < 0.5:
            pass
        for i in range(c):
            sys.stdout.write(str(random()) + " ")                   # volume [0 to 1]
            sys.stdout.write(str(round(random()*660) + 220) + " ")  # freq [220 to 880]
            sys.stdout.write(str(floor(random()*256)) + " ")        # instrument [0 to 255]
            sys.stdout.write(str(floor(random()*256)) + " ")        # automation [0 to 255]
        sys.stdout.write("\n")
        sys.stdout.flush()
        tn = time()
except KeyboardInterrupt:
    pass
