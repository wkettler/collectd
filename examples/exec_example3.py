#!/usr/bin/python

"""
exec_example3.py

Example collectd EXEC script.

Copyright (c) 2014  Nexenta Systems
William Kettler <william.kettler@nexenta.com>
"""

import os
import sys
import socket
import subprocess

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

# Start subprocess
producer = subprocess.Popen(['python', 'producer.py', str(interval)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

while True:
    # Read the next line from STDOUT
    values = producer.stdout.readline().strip()

    # Check subprocess status after reading stdout to prevent race condition
    # where process dies after checking status but before reading stdout
    if producer.poll() is not None:
        sys.stderr.write('ERROR subprocess has exited with retcode %s.\n'
                         % producer.retcode)
        sys.stderr.write(producer.stderr.read())
        sys.exit(1)

    # Print value to STDOUT
    sys.stdout.write('PUTVAL "%s/example3-py/gauge-rand_value" interval=%s '
                     'N:%s\n' % (hostname, interval, value))
    sys.stdout.flush()
