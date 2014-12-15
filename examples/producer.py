#!/usr/bin/python

"""
producer.py

Simple producer script that writes random values to STDOUT.

Copyright (c) 2014  Nexenta Systems
William Kettler <william.kettler@nexenta.com>
"""

import sys
from random import randint
from time import sleep

# Interval is passed as an argument
interval = float(sys.argv[1])

while True:
    # Generate a random value
    value = randint(0, 100)

    # Write value to STDOUT
    sys.stdout.write("%s\n" % value)
    sys.stdout.flush()

    # Sleep
    sleep(interval)
