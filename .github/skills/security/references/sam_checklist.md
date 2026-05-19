# SAM / CloudFormation Security Checklist

## IAM
- [ ] No `Action: "*"` in any policy
- [ ] No `Resource: "*"` in any policy
- [ ] Every policy scoped to specific resources

## Data at Rest
- [ ] DynamoDB: `SSEEnabled: true`
- [ ] S3: `ServerSideEncryptionConfiguration` present
- [ ] SQS: `KmsMasterKeyId` set

## Public Access
- [ ] S3: all 4 `PublicAccessBlock` flags set to `true`
- [ ] No `PublicRead` or `PublicReadWrite` ACLs
- [ ] RDS not publicly accessible

## Operational
- [ ] Every Lambda has DLQ configured
- [ ] CloudWatch log groups have `RetentionInDays` set
- [ ] `DeletionPolicy: Retain` on DynamoDB and S3
