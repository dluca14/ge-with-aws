### Steps for bootstrap and initialization of our pipeline using GitHub Actions.
1. Initialize bootstrap process:
```sam pipeline init --bootstrap```
2. Does your application contain any IMAGE type Lambda functions?
- choose: y
- Obs: you should already have 2 repos created for dev/prod with the naming convention: ge-${Stage}-repo
- In order to pass the repo-arn type this command in a different terminal window: 
```aws ecr describe-repositories```
3. What is the GitHub secret name for pipeline user account access key ID/secred?
- type: AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY

**Note:** 
1. The following resources were created in your account:
- Pipeline IAM user
- Pipeline execution role
- CloudFormation execution role
- Artifact bucket

2. You need to use the Security credentials of newly created Pipeline IAM user to config GitHub repo Secrets


## Find more info in this article:
https://www.antstack.io/blog/sam-pipeline-github-actions/