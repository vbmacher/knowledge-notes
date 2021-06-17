# HBase Compaction notes

https://www.slideshare.net/cloudera/hbasecon-2013-compaction-improvements-in-apache-hbase
https://blog.cloudera.com/introduction-to-apache-hbase-snapshots/


- HBase writes out immutable files as data is added
 - One of the main HBase design principles is that once a file is written it will never be modified. 
 
- Major compaction rewrites ALL files in a Store into one!
  - drop deleted records
  - tombstons old versions
  
- Minor compaction: files to compact are selected based on a heuristic
https://bitbucket.org/comniscient/relay-data-jobs/pull-requests/977/agg-2981-hbase-mappers-to-25-root-ebs-size)


# Restoring snapshot

https://blog.cloudera.com/introduction-to-apache-hbase-snapshots/

- restore a snapshot: This operation brings the table schema and data back to the snapshot state.
- The same principle applies to a Clone or Restore operation. Since the files are immutable a new table is created with just “links” to the files referenced by the snapshot.
- Export Snapshot is the only operation that require a copy of the data, since the other cluster doesn’t have the data files.
