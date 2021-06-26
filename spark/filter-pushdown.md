# Filter push-down

Does Spark optimize loading partitioned data if there's a partition-based filter downstream? Like, let's say we have
YMD-partitioned data. Is there a performance difference between:

- reading the full dataset, and doing a `filter('date.between(start, end))``, and
- reading the partial dataset by feeding a list of partitioned URLs to the `spark.read.parquet`?

Filter is pushed-down, also on S3, if:

- basePath is set
- filter() uses all partitions from the top
- filter() is first operation after read

