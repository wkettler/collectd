#!/usr/bin/python

"""
exec_example1.py

Example collectd EXEC script.

Copyright (c) 2014  Nexenta Systems
William Kettler <william.kettler@nexenta.com>
"""

import os
import sys
import socket
from time import sleep
from random import randint

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

while True:
    # Generate a random value
    value = randint(0, 100)

    # Print values to STDOUT
    sys.stdout.write('PUTVAL "%s/example1-py/gauge-rand_value" interval=%s '
                     'N:%s\n' % (hostname, interval, value))
    sys.stdout.flush()

    # Sleep
    sleep(interval)
