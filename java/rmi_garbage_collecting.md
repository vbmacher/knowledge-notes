https://docs.oracle.com/javase/7/docs/technotes/guides/rmi/faq.html#leases

- RMI uses distributed GC
- the GC uses a "lease" (prenajom) of remote RMI references which CLIENT holds
- the lease can be understood as a set of local RMI objects which have to be kept
  in memory (not gc-ed) because they can be used by client
- it renews the lease in some interval
- the leases are used for detecting abnormal client termination: if lease is not
  available after the lease interval, the strong ref to local object it is "unpinned"
  from RMI, so it is possible it will be gc-ed.


