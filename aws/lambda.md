# AWS Lambda

Serverless == Function as a Service (FaaS)

- Lambda
- DynamoDB
- AWS Cognito
- AWS API Gateway
- S3
- SNS & SQS
- Kinesos Data Firehose
- Aurora
- Step Functions
- Fargate


Lambda:
  - short executions
  - run on demand

pricing: per request and compute time

- up to 10GB of RAM
   - increasing RAM will improve CPU and network
   - 2 GB ... 2 CPU
   - 10 GB ... 6 CPU

- Max size of JAR file:
  - max 50 MB through web UI
  - max 250 MB unzipped from S3

- custom runtime API for other languages

- Lambda Container Image
  - the container image must implement Lambda Runtime API
  - ECS/Fargate is preferred for running arbitrary Docker images
  
  

