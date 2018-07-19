# Spark .toLocalIterator

 https://stackoverflow.com/questions/44053800/rdd-tolocaliterator-eager-evaluation

# Spark in IntelliJ Worksheet

https://stackoverflow.com/questions/36606273/duplicated-spark-context-with-intellij-in-worksheet


# Checking & validation on Azkaban
  
## check whether correct version is running:

When you upload to Azkaban, gradle prints project ID & version, e.g.:

Resuming previous Azkaban session
Once the zip is uploaded, Azkaban will validate your zip with Byte-Ray to complete the upload
Zip upload progress...
0%                20%                 40%                 60%                 80%                 100% (66267 KB)
|        |         |         |         |         |         |         |         |         |         |
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
--------------------------------------------------------------------------------
HTTP/1.1 200 OK [Content-Type: application/json, Content-Length: 46, Server: Jetty(6.1.26)] org.apache.http.conn.BasicManagedEntity@4e53c6ef
{  "projectId" : "151",  "version" : "142"}
--------------------------------------------------------------------------------
Zip /home/vbmacher/projects/funnel-fantasy-computations/workflow/build/distributions/workflow-azkaban-dev.zip uploaded successfully to https://azkaban.jsc.ff.avast.com:8443/manager?project=ffc-computations



projectId: 151, version: 142.

This can be checked on Azkaban, in Projects / Executions / Flow Log:

06-09-2017 15:26:59 CEST ff-computations INFO - Running execid:140345 flow:ff-computations project:151 version:142
06-09-2017 15:26:59 CEST ff-computations INFO - Update active reference
06-09-2017 15:26:59 CEST ff-computations INFO - Updating initial flow directory.
06-09-2017 15:26:59 CEST ff-computations INFO - Fetching job and shared properties.
06-09-2017 15:26:59 CEST ff-computations INFO - Starting flows
06-09-2017 15:26:59 CEST ff-computations INFO - Running flow 'ff-computations'.
06-09-2017 15:26:59 CEST ff-computations INFO - Configuring Azkaban metrics tracking for jobrunner object
06-09-2017 15:26:59 CEST ff-computations INFO - Submitting job 'ff-computations_spark' to run.

## Which action had run which tasks

- in logs, find DAGScheduler log which says e.g.:

 scheduler.DAGScheduler: Submitting 49 missing tasks from ResultStage 0 (MapPartitionsRDD[2] at parquet at ParquetDomain.scala:13)

# When some dependencies clash with Spark

- e.g. scalaz library

You can / should run your jar as a resource, not as code - get rid of the jar from the Spark's classpath

http://henningpetersen.com/post/22/running-apache-spark-jobs-from-applications


# java.lang.IllegalArgumentException: Size exceeds Integer.MAX_VALUE

https://stackoverflow.com/questions/42247630/sql-query-in-spark-scala-size-exceeds-integer-max-value

No Spark shuffle block can be larger than 2GB (Integer.MAX_VALUE bytes) so you need more / smaller partitions.

You should adjust spark.default.parallelism and spark.sql.shuffle.partitions (default 200) such that the number of partitions can accommodate your data without reaching the 2GB limit (you could try aiming for 256MB / partition so for 200GB you get 800 partitions). Thousands of partitions is very common so don't be afraid to repartition to 1000 as suggested.

https://www.slideshare.net/cloudera/top-5-mistakes-to-avoid-when-writing-apache-spark-applications/25


# Submit to cluster

        commandJob('spark-cluster') {
            uses 'spark2-submit ' +
                    '--deploy-mode cluster ' +
//                    '--executor-memory 6g ' +
                    '--master yarn ' +
                    '--files "${working.dir}/application.conf" ' +
//                    '--conf spark.yarn.executor.memoryOverhead=2048 ' +
//                    '--conf spark.yarn.driver.memoryOverhead=2048 ' +
//                    '--conf spark.driver.memory=6g ' +
                    '--class com.jumpshot.funnel.Runner ' +
                    '--conf "spark.driver.extraJavaOptions=' +
                    '-Dconfig.file=application.conf ' +
                    '-Dcomputation.from=${from} ' +
                    '-Dcomputation.to=${to} ' +
                    '-Dcomputation.type=per-domain" ' + sparkJar.name
        }



# Dynamic allocation investigation

http://jerryshao.me/2015/08/22/spark-dynamic-allocation-investigation/


































