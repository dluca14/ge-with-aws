# Great Expectations & AWS 
This project contains the setup that enables GE to work with AWS services (lambda, ECR, S3).
Lambda is a container-based function. The container is stored in ECR.
GE reads expectations from S3 (make sure you upload expectations in S3 bucket) and writes validation 
results as well as data-docs also in S3.

### The setup for this project contains the following 3 steps:
 - build Docker image containing Lambda Function dependencies and push it to ECR
 - building SAM CI/CD pipelines
 - configure SAM template for your AWS services

## Steps for building and deploying the project Docker image to ECR:
1. Build Docker image:
    ```docker build -t <image-tag> .```
   
2. Run container in detach mode and pass env-variables from `.env`:
    ```docker run --env-file .env -d -p 8080:8080 <image-tag>```
    
    **Optional:**
    - Enter container shell: ```docker exec -it <container_id> /bin/bash```
    - Test function locally: ```curl -XPOST "http://localhost:8080/2015-03-31/functions/function/invocations" -d '{}'```

3. Login to AWS-ECR:
   - aws version1:
   ```$(aws ecr get-login --no-include-email --region eu-central-1)```
   - aws version2:
   ```aws ecr get-login-password --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com```

4. Create ECR repository: 
    ```aws ecr create-repository --repository-name <repo-name>```
   
5. Rename Docker image to ECR format:
    ```docker tag <image-tag> <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/<image-tag>```

6. Push image to ECR registry:
    ```docker push <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/<image-tag>```


## Steps for bootstrap and initialization of project SAM-pipeline using GitHub Actions:
1. Initialize bootstrap process:
    ```sam pipeline init --bootstrap```
2. Does your application contain any IMAGE type Lambda functions?
    - choose: y
    - Obs: you should already have 2 repos created for dev/prod with the naming convention: ge-${Stage}-repo
    - In order to pass the repo-arn type this command in a different terminal window: 
```aws ecr describe-repositories```
3. What is the GitHub secret name for pipeline user account access key ID/secret?
    - type: AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY
4. After config completes edit resulted`.github/workflows/pipeline.yaml`:
 add `--parameter-overrides Stage=<stage_name> \` under `sam deploy` command according to stage.

**Results:** 
1. The following resources were created in your account:
    - Pipeline IAM user
    - Pipeline execution role
    - CloudFormation execution role
    - Artifact bucket
2. You need to use the Security credentials of newly created Pipeline IAM user to config GitHub repo Secrets.


## Config SAM `template.yaml`:
 - make sure you have the correct `arn` of your ECR image according to created `Stage`
 - make sure to config different buckets for GE output based on `Stack/Stage`

### Resources
   - https://www.antstack.io/blog/sam-pipeline-github-actions/
   - https://towardsdatascience.com/aws-lambda-with-custom-docker-images-as-runtime-9645b7baeb6f
   - https://docs.greatexpectations.io/docs/guides/setup/configuring_metadata_stores/how_to_configure_an_expectation_store_in_amazon_s3/
   - https://legacy.docs.greatexpectations.io/en/stable/guides/how_to_guides/configuring_data_docs/how_to_host_and_share_data_docs_on_s3.html