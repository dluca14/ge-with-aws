
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

### Note:
- you can add Authorization config for your ApiGateway:
```
 Auth:
   Authorizers:
     BasicAuthorizer:
       FunctionPayloadType: TOKEN
       FunctionArn: !ImportValue BasicAuthorizerFunction-Arn
       Identity:
         Header: Authorization
         ValidationExpression: ^[Bb]earer [-0-9a-zA-z\.]*$
         ReauthorizeEvery: 0
   DefaultAuthorizer: BasicAuthorizer
```
- you can add request validation in ApiGateway:
```
Resources:

  EchoWithValidationAPI:
    Type: AWS::Serverless::Api
    Properties:
      Name: echo-lpi-validate
      StageName: Prod
      TracingEnabled: True
      Models: 
        Inventor:
          type: object
          required:
            - name
            - wiki
          properties:
            name:
              type: string
            wiki:
              type: string
            knownFor:
              type: string

  EchoWithValidationFunction:
    Type: AWS::Serverless::Function 
    Properties:
      CodeUri: EchoFunctionJS
      Handler: app.lambdaHandler
      Runtime: nodejs10.x
      Events:
        Request:
          Type: Api 
          Properties:
            RestApiId: 
              Ref: EchoWithValidationAPI
            Path: /echo
            Method: post
            RequestModel:
              Model: Inventor
              Required: true

# more info here: https://github.com/mindit-io/aws-sam-serverless-services
```
- you can make a custom Domain for your ApiGateway Output: for this you need to register a domain in `Route 53`
```
ExampleApiCertificate:
  Type: AWS::CertificateManager::Certificate
  Properties:
    DomainName: api.example.com
    ValidationMethod: DNS

YourApiGateway:
 Properties:
   Domain:  # https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html
     DomainName: www.example.com
     CertificateArn: !Ref ExampleApiCertificate
     BasePath:
       - foo
       - bar                
```

### Resources:
- https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification-template-anatomy.html

