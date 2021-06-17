# VPC

- it is region-based. In each region must be differen VPC
- has VPC CIDR range (range of IPs for whole VPC) per region

- inside VPC create subnets: private, public
- a subnet lies in availability zone; in one region can be multiple AZs

- public subnets have access to internet using Internet Gateway
- private subnets have access to internet using:
  - AWS-managed NAT gateways
  - self-managed NAT instances

  1. deploy our NAT gateway or NAT instance in our public subnet
  2. add route from private subnet to the NAT in public subnet

- NACL: Network ACL - "access control list"
  - at subnet level
  - firewall
  - rules can have ALLOW/DENY
  - rules can contain only IP addresses
  
- Security groups
  - at instance level (can be deployed later)
  - come from ENI (Elastic Network Interface) or EC2
  - can have only ALLOW rules
  - rules can contain IP addresses or other security groups


- VPC Flow logs
  - capture logs from all IP traffic; also from managed AWS services
  - can go to S3 or Cloudwatch
  - VPC flow logs
  - subnet flow logs
  - ENI flow logs
  
  
- VPC Peering
  - connect multiple VPCs as if they were on the same network
  - must not have overlapping CIDRs
  - VPC Peering is not transitive; must be set up on each VPC
  
- VPC Endpoints
  - allow you to connect to AWS Services using private network
  - VPC Endpoint Gateways:
    - only for S3 and DynamoDB
    - installed in VPC level
  - VPC Endpoint Interfaces (ENI):
    - the rest of AWS services
    - installed in the private subnet level
     

