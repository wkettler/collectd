#!/usr/bin/python

"""
exec_mpstat.py

collectd EXEC script that monitors CPU performance.

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
producer = subprocess.Popen(["/usr/bin/mpstat",
                            str(interval)], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

# Define the output fields from nfsmon.d
keys = ["minf", "mjf", "xcal", "intr", "ithr", "csw", "icsw", "migr", "smtx",
        "srw", "syscl", "usr", "sys", "wt", "idl"]

while True:
    # Read the next line from STDOUT
    line = producer.stdout.readline()

    # Check subprocess status after reading stdout to prevent race condition
    # where process dies after checking status but before reading stdout
    if producer.poll() is not None:
        sys.stderr.write('ERROR subprocess has exited with retcode %s.\n'
                         % producer.retcode)
        sys.stderr.write(producer.stderr.read())
        sys.exit(1)

    # Parse the stats
    try:
        values = [int(x.strip()) for x in line.split()]
    # mpstat header will raise a ValueError
    except ValueError:
        continue
    cpu = values.pop(0)
    stats = dict(zip(keys, values))

    # Print values to STDOUT
    for key, value in stats.iteritems():
        sys.stdout.write('PUTVAL "%s/mpstat/gauge-%s-%s" interval=%s '
                         'N:%s\n' % (hostname, cpu, key, interval, value))
    sys.stdout.flush()
