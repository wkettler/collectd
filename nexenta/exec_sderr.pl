#!/usr/bin/perl
#
# exec_sderr.pl
#
# collectd EXEC script that monitors sd errors.
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
my $host     = '';
my $interval = 0;
my $sdref    = 0;
my $hard     = 0;
my $soft     = 0;
my $trans    = 0;

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
    $sdref = $kstat->{sderr};
    foreach my $key (keys %$sdref) {
        $hard  = $sdref->{$key}->{"sd${key},err"}->{"Hard Errors"};
        $soft  = $sdref->{$key}->{"sd${key},err"}->{"Soft Errors"};
        $trans = $sdref->{$key}->{"sd${key},err"}->{"Transport Errors"};

        print "PUTVAL \"$host/disk_sd${key}/gauge-h_w\" interval=$interval ",
              "N:$hard\n";
        print "PUTVAL \"$host/disk_sd${key}/gauge-s_w\" interval=$interval ",
              "N:$soft\n";
        print "PUTVAL \"$host/disk_sd${key}/gauge-trn\" interval=$interval ",
              "N:$trans\n";
    }

    # Sleep
    sleep $interval;
}
