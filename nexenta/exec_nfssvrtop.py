#!/usr/bin/python

"""
exec_nfssvrtop.py

collectd EXEC wrapper for the modified version of nfssvrtop.

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
producer = subprocess.Popen(["/usr/local/collectd/bin/nfssvrtop",
                            str(interval)], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

time = 0
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

    # Get timestamp
    if line.startswith("time"):
        time = line.split(",")[1].strip()
        continue

    key, value = [x.strip() for x in line.split(",")]
    sys.stdout.write('PUTVAL "%s/nfssvrtop/%s" %s:%s\n' % (hostname, key, time,
                                                           value))
    sys.stdout.flush()
