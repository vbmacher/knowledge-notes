# Computing Apache Spark parameters

## How Apache Spark works

### Code

A Spark application is split into executors, which can run on one or more nodes. They are driven by a "driver", which is responsible for coordination of tasks, job planning, broadcasting data and collection of results (when we call reduce/collect operations).

One executor is a JVM process - a "container", communicating with the driver though RPC (remote-procedure-call). An executor can run one or more tasks. Since executor is a JVM process, it has defined its memory limits and CPU limits (cores = number of threads).

A task:
- runs on 1 thread on an executor
- consumes 1 partition of data (from the input, or shuffle files)
- is outputting so-called shuffle files (intermediate results; either in memory or disk) or the output
- executor can run 1 or more tasks simultaneously (depends on `spark.executor.cores`) and in theory the tasks can read different data. In practice Spark groups tasks which operate on the same data in one executor for performance reasons. 

### Data

Data which Spark application processes is also split - into so-called partitions. Initially, the number of partitions is given by the input - e.g. number of parquet files. Later, number of partitions can change - it will depend on various things:

- type of operation (e.g. HashJoin, GroupBy, Distinct etc. vs. repartition, coalesce, countByKey)
- number of shuffle partitions (`spark.sql.shuffle.partitions`) - outputs
- data itself - e.g. GroupBy creates number of partitions equal to the cartesian product of all values of all columns in the GroupBy, but possibly reduced by so-called Map-Side Reduction optimization.

### Job flow

A job is composed of stages, or "layers" of computation. Some operations cannot be performed in single pass, so that's why we need stages. A stage then consists of tasks which need to be done. In theory only after all tasks are done in a stage, the computation can follow with the next stage. In practice, when some tasks finish, and they serve as inputs to the next stage, the next stage can start before the previous ends (another optimization). 

## Tuning Executor-oriented parameters

There exist several approaches:

- CPU-based
- memory-based

### CPU-based approach

In CPU-oriented approach, we are trying to maximize tasks run on an executor. With some "general" knowledge, it is widely used `spark.executor.cores=5`. The strategy is to start with computing number of executors based on the number of available CPUs, and then derive the maximum amount of memory for the executor:

```
coresPerExecutor = 5
executorsPerNode = (nodeCpus - 1) / coresPerExecutor  // -1 because we want to keep 1 thread for the OS
executors = executorsPerNode * nodesCount 

memoryPerExecutor = nodeMemory / executorsPerNode
memoryOverhead = max(0.384, 0.07 * memoryPerExecutor)
executorMemory = memoryPerExecutor - memoryOverhead
```

This approach has the following properties:
- maximum parallelism is: `executors * coresPerExecutor = 5 * executors`
- if there is just 1 task running on an executor, the partition can be `memoryPerExecutor` big
- if there are `coresPerExecutor` tasks run on an executor (=5), the partition can be `memoryPerExecutor/coresPerExecutor` big.

When thinking about what can go wrong in performance, this approach can be:
- *under-performing*: if `(partition1Task1 size) + ... + (partitionNTaskN size) < memoryPerExecutor` we allocate unnecessarily too much memory  
- *not-well-performing*: if we see data spills (on disk), then we are not-well-performing. Executor memory is too small to hold data of all tasks in memory. Disk spills are also connected with garbage collections.

### Memory-oriented approach

In the memory-oriented approach, we basically "shrink" executor to perform just one task, but we instead try to add as many executors as possible. In this case we must know the maximum memory which any task in the job needs. This can be hard to find out, because the task memory does not depend only on the input, but also on the task itself - we can have:
- "reduction" tasks - result is smaller than input
- "explosive" tasks - result is bigger than input (or internal computation generates intermediate data bigger than input)

But if we know the memory (e.g. by trying), we can compute everything as follows:

```
coresPerExecutor = 1
memoryPerExecutor = XX GB  // we know that
memoryOverhead = max(0.384, 0.07 * memoryPerExecutor)
executorMemory = memoryPerExecutor - memoryOverhead

executorsPerNode = min(nodeCpus, floor(nodeMemory/memoryPerExecutor)) - 1
executors = executorsPerNode * nodesCount
```

This approach has the following properties:
- maximum parallelism is: `executors`
- each executor can execute just 1 task
- it is easier to control executor memory of 1 task than of multiple ones
- small-memory tasks will still consume whole executor

## Tuning Data-oriented parameters

The main parameter which should be tuned is:

- `spark.sql.shuffle.partitions`

Byt default it is 200, but in reality it is almost never right. The partition size should be >= 128 MB and < 1GB.

