SQS

- unlimited throughput
- unlimited messages in the queue

- retention means: must be read until the retention period
- low < 10ms latency
- max 256KB per message

- at least once delivery (dupes might exist)
- can have out of ordering

- receivers can poll up to 10 messages at a time
- consumer must call DeleteMessage through API
  - or wait on retention



