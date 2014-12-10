#!/bin/bash
#
# exec_example1.sh
#
# Example collectd EXEC script.
#
# Copyright (c) 2014  Nexenta Systems
# William Kettler <william.kettler@nexenta.com>
#

HOSTNAME="${COLLECTD_HOSTNAME:-$(hostname -f)}"
INTERVAL="${COLLECTD_INTERVAL:-10}"

while sleep "${INTERVAL}"
do
    VALUE=$RANDOM
    echo -n "PUTVAL \"${HOSTNAME}/example1-sh/gauge-rand_value\" interval=${INTERVAL} N:${VALUE}"
done
