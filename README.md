# Great Expectations & AWS 

This project contains the setup that enables GE to work with AWS services (lambda, ECR, S3).
Lambda is a container-based function. The container is stored in ECR.
GE reads expectations from S3 (make sure you upload expectations in S3 bucket) and writes validation 
results as well as data-docs also in S3.

### Deployment:
   - Container: using aws-cli
   - Lambda: using aws-sam-cli

### Steps for building and deploying the project:

1. Build Docker image:
```docker build -t <image-tag> .```
   
2. Run container in detach mode and pass env-variables from .env:
```docker run --env-file .env -d -p 8080:8080 <image-tag>```
   
    Optional:
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

7. Create lambda function using AWS-SAM-CLI:
```sam deploy --guided```
   

### Resources
   - https://towardsdatascience.com/aws-lambda-with-custom-docker-images-as-runtime-9645b7baeb6f
   - https://docs.greatexpectations.io/docs/guides/setup/configuring_metadata_stores/how_to_configure_an_expectation_store_in_amazon_s3/
   - https://legacy.docs.greatexpectations.io/en/stable/guides/how_to_guides/configuring_data_docs/how_to_host_and_share_data_docs_on_s3.html