# EMR

- instance groups:
  - measured through number of instances
- instance fleets:
  - offers the widest variety of provisioning options for EC2 instances
  - For each instance fleet, you may specify up to five instance types
  - you specify target capacities. when cluster launches EMR provisions instances until the targets are fulfilled
  - we can use multiple subnets for different AZs. EMR looks across subnets to find instances and specified purchasing options 
  - measured throug "generic units" - you specifiy units to each instance type (meaning - something like "weight", e.g. bigger instance type=more units) and defining target capacity is in terms of units, 


- EMR-managed scaling:
  - master node cannot be scaled after initial configuration
  - minimum/maximum: by vCPUs or no. of instances in instance groups. 
  - works only in YARN applications (Spark, Hadoop, Hive, Flink)
  
