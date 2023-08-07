#!/usr/bin/python3
import sys
from random import random
from time import time

tn = 0

try:
    while True:
        while time() - tn < 0.5:
            pass
        sys.stdout.write(str(round(random()*660) + 220) + "\n")
        sys.stdout.flush()
        tn = time()
except KeyboardInterrupt:
    pass
