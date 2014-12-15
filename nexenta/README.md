collectd
========

A collection of collectd Nexenta scripts.

---

A note about the *svrtop scripts.

The *svrtop collectd implementation posed several issues. The original implemenation used Korn Shell, i.e. ksh, which when launched by collectd would peg the CPU while continuously trying to open a specific file descriptor. The scripts were changed to use bash however collectd only appears to read the stdout stream of the parent process. Ultimately a producer/consumer model was used.

The *svrtop EXEC scripts have not been tested in large deployments for performance impact but it is possible that hundreds or thousands of clients could cause a performance impact on the system.
