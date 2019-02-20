In the situation in which:

- there was performed some work already in the job,
- and cluster/YARN has enough resources
- and it takes too long to start new stage/task,

The reason for this might be in too low DRIVER MEMORY. Garbage collector tries hard
to free some memory. Sometimes it might succeed, sometimes not and it crashes on OOM
in possibly long time.

The solution should involve two considerations:

1. Increase driver memory
2. Lower the GC overhead limit, to crash sooner and not make GC suffer for long time.


