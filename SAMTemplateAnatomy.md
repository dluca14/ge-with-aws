
### Template structure:
- Transform declaration: This declaration identifies an AWS CloudFormation template file as an AWS SAM template file
- Parameters section: Objects that are declared in the Parameters section allow the sam deploy --parameters-overrides ParamName=value command to present specific values for every Stage defined in SAM pipeline. 
- Globals section: It defines properties that are common to all your serverless functions and APIs. 
- Resources section: This section can contain a combination of AWS CloudFormation resources and AWS SAM resources.
- Outputs section: The values that are returned whenever you view your stack's properties.

**Note** that the template is configured in such a way that it allows SAM-pipeline to to build CloudFormation stacks dynamically based on the [Stage] and [StackName].

-------------------------------------------------------------------------------------------------------------------------------------------------
```
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: template-description

Parameters:
 Stage:
   Type: String
   Default: dev

Globals:
 Function:
  Timeout: 45
  MemorySize: 512

Resources:
 NameApiGateway:
  Type: AWS::Serverless::Api
  Properties:
    Name: !Sub NameApiGateway-${AWS::StackName}
    StageName: !Ref Stage # The stage name will be passed as an param on sam deploy when building the pipelines

 NameFunction:
   Type: AWS::Serverless::Function
   Properties:
     FunctionName: !Sub YourFunctionName-${AWS::StackName}
     ImageUri: !Sub <aws-account>.dkr.ecr.<aws-region>.amazonaws.com/ge-${Stage}-repo:latest
     PackageType: Image
     Events:
       EventName:
         Type: Api
         Properties:
           RestApiId: !Ref NameApiGateway # tells the Lambda to attach to the created API Gateway.
           Path: /<your_resource>
           Method: <your_method>
     Policies:
       - S3FullAccessPolicy:
           BucketName: <bucket-name> # bucket name without arn
       - S3FullAccessPolicy:
           BucketName: <bucket-name> # bucket name without arn
       - S3FullAccessPolicy:
           BucketName: <bucket-name> # bucket name without arn

Outputs:
  GEValidationsApiGateway:
  Description: 'API Gateway description'
  Value: !Sub 'https://${NameApiGateway}.execute-api.${AWS::Region}.amazonaws.com/${Stage}/<your_resource>/'
```
----------------------------------------------------------------------------------------------------------------------------------------------------------

### Resources:
- https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification-template-anatomy.html

