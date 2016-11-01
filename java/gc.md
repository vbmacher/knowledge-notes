http://www.cubrid.org/blog/dev-platform/understanding-java-garbage-collection/

# Memory allocations in JVM:

- Young generation (allocations goes here, with max size)
- Old generation (survivors after several runs of GC)
- Permanent generation (methods, classes, string constants)


- minor GC: young gen GC
- major or full GC: old or perm gen GC


## Young generation

- Eden space
- 2 Survivor spaces

Eden space contain all new objects. 2 allocation algorithms:

- bump-the-pointer, not thread safe. Objects are in queue, new one replaces the "last" one
- TLAB (Thread-Local allocation buffers) - thread safe. Threads have smaller local "edens"


- fast GC
- looks up the "card table" (512-byte cache), which contains references from old gen to young gen

## Old generation

- GC is run only when data is full


# Monitoring GC

It is worth of monitoring:
- when an object in young has moved to old and by how much
- when stop-of-the-world has occured and for how long



# interesting things

- GC Overhead means: JVM spend more than XX% of time doing GC instead of useful work
    --> it does not mean OutOfMemory


