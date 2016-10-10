http://help.eclipse.org/mars/index.jsp?topic=/org.eclipse.mat.ui.help/welcome.html

NOTE: Java8 heapdumps crash with MAT, there exists another tool:
  
  https://www.ibm.com/developerworks/community/groups/service/html/communityview?communityUuid=4544bafe-c7a2-455f-9d43-eb866ea60091

  It's called: IBM HeapAnalyzer



shallow_heap - memory consumed by 1 object
retained set (X) - set of objects which will be removed by gc when X is gc-ed
  - it is something like objects which are strongly connected
  - it is practically a directed graph (can be cyclic)

retained heap of X - is memory consumed by the retained set (sum of all shallow heaps in X)


example:
 object A has its shallow heap (how much it consumes memory), but also retained size - how much memory will be
 freed when GC is called => retained size considers all other objects which can be freed when this A object is freed.

leading set - set of objects in which all elements TOGETHER (not one by one) "holds" a retained (sub-)set
  - practically is the "root" - beginning of the (sub-)graph

garbage collection roots - is practically a leading set in which elements don't have parents, each element in the set is
                           called a "gc root" (so not the set itself is called that way)
  - can be: local parameters, local objects, objects used for wait(), notify(), synchronized(), etc.
  - can be understood as the "base" of the "house" of retained heap. By invalidating the complete set, the retained set is
    "freed"

dominator tree
--------------

http://help.eclipse.org/mars/index.jsp?topic=/org.eclipse.mat.ui.help/welcome.html

An object x dominates an object y if every path in the object graph from the start (or the root) node to y must go through x.

The immediate dominator x of some object y is the dominator closest to the object y.

dominator tree is build from the object graph, in this way:
  - we start from imaginary root, and try to find every way to each node separately.
  - we remember all nodes which are shared in all the ways
  - the closest shared node to the goal node is called "immediate dominator"
  - we build the dominator tree starting with the imaginary node with arrows through immediate dominators to resulting nodes.
  - if a node donesn't have a immediate dominator, it must be accessed from the root "imaginary" node (if not, it does not belong to the retained set at all)

properties of dom. trees:
  - The objects belonging to the sub-tree of x (i.e. the objects dominated by x ) represent the retained set of x .
  - If x is the immediate dominator of y , then the immediate dominator of x also dominates y , and so on.
  - The edges in the dominator tree do not directly correspond to object references from the object graph.


garbage collection roots
------------------------

http://help.eclipse.org/mars/index.jsp?topic=/org.eclipse.mat.ui.help/welcome.html

A garbage collection root is an object that is accessible from outside the heap. The following reasons make an object a GC root:
  - system class - Class loaded by bootstrap/system class loader. For example, everything from the rt.jar like java.util.* .
  - JNI locali - Local variable in native code, such as user defined JNI code or JVM internal code.
  - JNI global - Global variable in native code, such as user defined JNI code or JVM internal code.
  - thread block -  Object referred to from a currently active thread block.
  - thread - A started, but not stopped, thread.
  - busy monitor - Everything that has called wait() or notify() or that is synchronized. For example, by calling synchronized(Object) or by entering a synchronized method. Static method means class, non-static method means object.
  - java local - Local variable. For example, input parameters or locally created objects of methods that are still in the stack of a thread.
  - native stack
  - finalizable - An object which is in a queue awaiting its finalizer to be run.
  - unfinalized - An object which has a finalize method, but has not been finalized and is not yet on the finalizer queue.
  - unreachable - An object which is unreachable from any other root, but has been marked as a root by MAT to retain objects which otherwise would not be included in the analysis.
  - java stack frame
  - unknown - 


