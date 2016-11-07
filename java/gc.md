http://www.cubrid.org/blog/dev-platform/understanding-java-garbage-collection/

http://blog.takipi.com/garbage-collectors-serial-vs-parallel-vs-cms-vs-the-g1-and-whats-new-in-java-8/?utm_source=blog&utm_medium=in-post&utm_content=java9top&utm_campaign=java


# Memory allocations in JVM:

- Young generation (allocations goes here, with max size)
- Old generation (survivors after several runs of GC)
- Permanent generation (methods, classes, string constants)

- minor GC: young gen GC
- major or full GC: old or perm gen GC

In Java 8, permgen was removed.


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

# Garbage collectors

- Serial: single threaded, is not used by default (-XX:+UseSerialGC)

- Parallel / Throughput collector. Multi-threaded. Will do STW on minnor/major GC. It is default.

- CMS (concurrent mark-and-sweep). Multi-threaded, two-steps. First marks objects, then
  sweeps them. Goal: minimize STW. Potential "promotion failures". Usable if heap size < 4GB
  (-XX:+USeParNewGC)

- G1: designed to support heaps > 4GB. Divide heaps into regions from 1-32MB. Scans bigger
  regions with more garbage first (therefore Garbage First, G1). It compacts heap on the go,
  what others do only when STW occurs.
  (-XX:+UseG1GC). 

- G1 can de-duplicate String constants:  -XX:+UseStringDeduplicationJVM 

- How G1 works: https://www.infoq.com/articles/G1-One-Garbage-Collector-To-Rule-Them-All

# Monitoring GC

It is worth of monitoring:
- when an object in young has moved to old and by how much
- when stop-of-the-world has occured and for how long



# interesting things

- GC Overhead means: JVM spend more than XX% of time doing GC instead of useful work
    --> it does not mean OutOfMemory


