#!/usr/bin/python

"""
exec_example2.py

Example collectd EXEC script.

Copyright (c) 2014  Nexenta Systems
William Kettler <william.kettler@nexenta.com>
"""

import os
import sys
import socket
from time import sleep
from random import randint


def get_counter():
    """
    A random generator that counts up.

    Inputs:
        None
    Outputs:
        v (int): Random value
    """
    v = 0
    while True:
        yield v
        v += randint(0, 100)

# Get the system hostname
if 'COLLECTD_HOSTNAME' in os.environ:
    hostname = os.environ['COLLECTD_HOSTNAME']
else:
    hostname = socket.gethostname()

# Define the polling interval
if 'COLLECTD_INTERVAL' in os.environ:
    interval = int(float(os.environ['COLLECTD_INTERVAL']))
else:
    interval = 10

# Define counter and seed the first value
counter = get_counter()
prev = counter.next()

while True:
    # Sleep
    sleep(interval)

    # Calculate average over previous interval
    cur = counter.next()
    avg = (cur - prev) / interval

    # Print values to STDOUT
    sys.stdout.write('PUTVAL "%s/example2-py/gauge-rand_value" interval=%s '
                     'N:%s\n' % (hostname, interval, avg))
    sys.stdout.flush()

    # Set previous to current
    prev = cur
