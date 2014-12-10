#!/usr/bin/perl
#
# exec_example1.pl
#
# Example collectd EXEC script.
#
# Copyright (c) 2014  Nexenta Systems
# William Kettler <william.kettler@nexenta.com>
#

use strict;
use warnings;
use Sys::Hostname;

# Ubuffered stdout
$| = 1;

# Variable declerations
my $host     = '';
my $interval = 0;
my $value    = 0;

# Define the system hostname
if (defined $ENV{'COLLECTD_HOSTNAME'}) {
    $host = $ENV{'COLLECTD_HOSTNAME'};
} else {
    $host = hostname;
}

# Define the polling interval
if (defined $ENV{'COLLECTD_INTERVAL'}) {
    $interval = int($ENV{'COLLECTD_INTERVAL'});
} else {
    $interval = 10;
}

while (1) {
    # Generate a random value
    $value = int(rand(100));

    # Print values to STDOUT
    print "PUTVAL \"$host/example1-pl/gauge-rand_value\" interval=$interval ",
          "N:$value\n";

    # Sleep
    sleep $interval;
}
