#!/usr/bin/python

"""
exec_iostat.py

collectd EXEC that monitors disk performance using iostat.

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
producer = subprocess.Popen(['/usr/bin/iostat', '-x', str(interval)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# iostat columns excluding device
keys = ["r_s", "w_s", "kr_s", "kw_s", "wait", "actv", "svc_t", "pct_w",
        "pct_b"]

while True:
    # Read the next line from STDOUT
    line = producer.stdout.readline().strip()

    # Check subprocess status after reading stdout to prevent race condition
    # where process dies after checking status but before reading stdout
    if producer.poll() is not None:
        sys.stderr.write('ERROR subprocess has exited with retcode %s.\n'
                         % producer.retcode)
        sys.stderr.write(producer.stderr.read())
        sys.exit(1)

    # Ignore headers
    if line.startswith("device") or line.startswith("extended"):
        continue

    # Parse stats
    values = [x.strip() for x in line.split()]
    device = values.pop(0)
    stats = dict(zip(keys, values))

    # Print values to STDOUT
    for key, value in stats.iteritems():
        sys.stdout.write('PUTVAL "%s/iostat/gauge-%s-%s" interval=%s '
                         'N:%s\n' % (hostname, device, key, interval, value))
    sys.stdout.flush()
