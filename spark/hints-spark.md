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


# java.lang.InternalError: Malformed class name

Combination of:

https://gist.github.com/tzachz/c976a1080b6379ef861c142c16f1364a

and:

https://stackoverflow.com/questions/42735617/how-to-write-an-encoder-for-a-collection-in-spark-2-1


I want to aggregate `Map[K, Seq[V]]` in `groupBy`:

```
  dataset.groupBy('something).agg(mergeMaps('themap))

```

For this, I need to define UDAF `mergeMaps`. Example:


```
case class NameCount(name: String, count: Long)

case class X(value: Seq[NameCount])


// Now - either (wanted):
//
//  case class Y(a: String, b: Map[Int, Seq[NameCount]])
//
// - or - (works :/ )

case class Y(a: String, b: Map[Int, X])


// ...

    import spark.implicits._

    val ss = Seq(
      Y("a", Map(1 -> X(Seq(NameCount("a", 1))))),
      Y("a", Map(1 -> X(Seq(NameCount("a", 1)))))
    ).toDS()


    implicit val enc = Encoders.product[NameCount]

    val mergess = new MergeMapsStructUDAF[Int, Seq[NameCount]](IntegerType, {
      case (fst, snd) =>
        val fstMap = fst.map(nc => (nc.name, nc.count)).toMap
        val sndMap = snd.map(nc => (nc.name, nc.count)).toMap

        val rawResult = fstMap ++ sndMap.map { case (k, v) => k -> fstMap.get(k).map(v + _).getOrElse(v) }
        rawResult.toSeq.map { case (name, count) => NameCount(name, count) }
    })

    ss.groupBy('a).agg(mergess('b)).show()   // java.lang.InternalError: Malformed class name ?!!!
```

After debugging - it seems it's exception when creating another exception, from calling
`getCanonicalName`:

```
     case other => throw new IllegalArgumentException(
          s"The value (${other.toString}) of the type (${other.getClass.getCanonicalName}) "
            + s"cannot be converted to an array of ${elementType.catalogString}")

```

^ Which is the real one.

Solution:

Arrays in maps are wrapped in struct by spark itself!!! The UDAF looks like:

```
class MergeMapsStructUDAF[K, V: Encoder](keyType: DataType, merge: (V, V) => V) extends UserDefinedAggregateFunction {
  private implicit val enc = implicitly[Encoder[V]]

  private val rowEncoder = RowEncoder(enc.schema)
  private val valueEncoder = enc.asInstanceOf[ExpressionEncoder[V]].resolveAndBind()

  override def inputSchema: StructType = new StructType().add("map", dataType)

  override def bufferSchema: StructType = inputSchema

  override def dataType: DataType = MapType(keyType, enc.schema)

  override def deterministic: Boolean = true

  override def initialize(buffer: MutableAggregationBuffer): Unit = buffer(0) = Map.empty[K, V]

  override def update(buffer: MutableAggregationBuffer, input: Row): Unit = {
    val map1 = buffer.getAs[Map[K, GenericRowWithSchema]](0)        // Simple V doesn't work :(
      .mapValues(r => valueEncoder.fromRow(rowEncoder.toRow(r)))    
    val map2 = Option(input.getAs[Map[K, GenericRowWithSchema]](0))  // Simple V doesn't work :(
      .getOrElse(Map.empty[K, GenericRowWithSchema])
      .mapValues(r => valueEncoder.fromRow(rowEncoder.toRow(r)))

    buffer.update(0, mergeMaps[K, V](map1, map2, merge))
  }

  override def merge(buffer1: MutableAggregationBuffer, buffer2: Row): Unit = update(buffer1, buffer2)

  override def evaluate(buffer: Row): Any = buffer.getAs[Map[K, V]](0)  // This works...
}
object MergeMapsStructUDAF {

  def mergeMaps[K, V](map1: Map[K, V], map2: Map[K, V], merge: (V, V) => V): Map[K, V] = {
    map1 ++ map2.map { case (k,v) => k -> map1.get(k).map(merge(_, v)).getOrElse(v) }
  }

  def apply[K, V: Encoder](keyType: DataType, merge: (V, V) => V): MergeMapsStructUDAF[K, V] = {
    new MergeMapsStructUDAF(keyType, merge)
  }
}
```























