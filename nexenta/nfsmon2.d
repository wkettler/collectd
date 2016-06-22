#!/usr/sbin/dtrace -s

#pragma D option quiet

/*
 * nfsmon.d
 *
 * Monitor NFS read/write and getattr performance.
 *
 * All latencies are reported in nanosecs.
 *
 * Copyright (c) 2016  Nexenta Systems
 * William Kettler <william.kettler@nexenta.com>
 *
 */

inline int INTERVAL = $1;

dtrace:::BEGIN
{
    secs = INTERVAL;
}

nfsv3:::op-read-start,
nfsv3:::op-write-start,
nfsv3:::op-getattr-start
{
    self->start = timestamp;
}

nfsv3:::op-read-done
/self->start/
{
    @r_latency["r_latency", INTERVAL] = avg(timestamp - self->start);

    self->start = 0;
}

nfsv3:::op-write-done
/self->start/
{
    @w_latency["w_latency", INTERVAL] = avg(timestamp - self->start);

    self->start = 0;
}

nfsv3:::op-getattr-done
/self->start/
{
    @g_latency["g_latency", INTERVAL] = avg(timestamp - self->start);

    self->start = 0;
}

profile:::tick-1sec
{
	secs--;
}

profile:::tick-1sec
/secs == 0/
{
    printa("PUTVAL \"nfs/nfsv3/%s\" interval=%i N:%@d\n", @r_latency);
    printa("PUTVAL \"nfs/nfsv3/%s\" interval=%i N:%@d\n", @w_latency);
    printa("PUTVAL \"nfs/nfsv3/%s\" interval=%i N:%@d\n", @g_latency);

    clear(@r_latency);
    clear(@w_latency);
    clear(@g_latency);

    secs = INTERVAL;
}
