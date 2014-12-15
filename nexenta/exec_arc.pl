#!/usr/bin/perl
#
# exec_arc.pl
#
# collectd EXEC script that monitors arc statistics.
#
# Copyright (c) 2014  Nexenta Systems
# William Kettler <william.kettler@nexenta.com>
#

use strict;
use warnings;
use Sys::Hostname;
use Sun::Solaris::Kstat;

# Ubuffered stdout
$| = 1;

# Variable declerations
my $host         = '';
my $interval     = 0;
my $arc_hits     = 0;
my $arc_misses   = 0;
my $meta_used    = 0;
my $meta_limit   = 0;
my $l2arc_size   = 0;
my $l2arc_hits   = 0;
my $l2arc_misses = 0;

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

# Initialize kstats
my $kstat = Sun::Solaris::Kstat->new();

while (1) {
    # Update kstats
    $kstat->update();

    # Read arc kstats
    $arc_hits   = ${kstat}->{zfs}->{0}->{arcstats}->{hits};
    $arc_misses = ${kstat}->{zfs}->{0}->{arcstats}->{misses};
    $meta_used  = ${kstat}->{zfs}->{0}->{arcstats}->{arc_meta_used};
    $meta_limit = ${kstat}->{zfs}->{0}->{arcstats}->{arc_meta_limit};

    # Print values to STDOUT
    print "PUTVAL \"$host/arc/derive-arc_hits\" interval=$interval ",
          "N:$arc_hits\n";
    print "PUTVAL \"$host/arc/derive-arc_misses\" interval=$interval ",
          "N:$arc_misses\n";
    print "PUTVAL \"$host/arc/gauge-meta_used\" interval=$interval ",
          "N:$meta_used\n";
    print "PUTVAL \"$host/arc/gauge-meta_limit\" interval=$interval ",
          "N:$meta_limit\n";

    # Don't waste cycles if l2arc doesn't exist
    $l2arc_size = ${kstat}->{zfs}->{0}->{arcstats}->{l2_size};
    if ($l2arc_size != 0) {
        # Read l2arc stats
        $l2arc_hits   = ${kstat}->{zfs}->{0}->{arcstats}->{l2_hits};
        $l2arc_misses = ${kstat}->{zfs}->{0}->{arcstats}->{l2_misses};

        # Print values to STDOUT
        print "PUTVAL \"$host/arc/derive-l2_arc_hits\" interval=$interval ",
              "N:$l2arc_hits\n";
        print "PUTVAL \"$host/arc/derive-l2_arc_misses\" interval=$interval ",
              "N:$l2arc_misses\n";
     }

    # Sleep
    sleep $interval;
}
