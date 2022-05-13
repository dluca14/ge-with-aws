# API Gateway
 - API Gateway provides tools for creating and documenting web APIs that route HTTP requests to Lambda functions. 
 - You can secure access to your API with authentication and authorization controls. 
 - Your APIs can serve traffic over the internet or can be accessible only within your VPC.

### Manually create API Gateway:
1. Open the Functions page of the Lambda console.
2. Choose a function.
3. Under Functional overview, choose Add trigger.
4. Select API Gateway.
5. For API, choose Create an API.
6. For API type, you can choose HTTP or REST API. 
7. For Security, you can choose: IAM, Open, API key. 
8. Choose Add.

### Configure API Gateway through SAM template.yml
```
Resources:
  ExampleApiCertificate:
    Type: AWS::CertificateManager::Certificate
    Properties:
      DomainName: api.example.com
      ValidationMethod: DNS
  GeApiGateway:
    Type: AWS::Serverless::Api
    Properties:
      Name: GE Validations Api Gateway
      StageName: Staging  # The stage and resource determine the path of the endpoint: /Staging/validation
      Domain:  # https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html
        DomainName: www.example.com  # create domain in Route 53
        CertificateArn: !Ref ExampleApiCertificate
        BasePath:
          - foo
          - bar
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
  LambdaFunctionName:
    Events:
      EventName:
        Type: Api # More info about API Event Source: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
        Properties:
          RestApiId: !Ref GeApiGateway
          Path: /your_path_name
          Method: get
Outputs:
  # ServerlessRestApi is an implicit API created out of Events key under Serverless::Function
  # Find out more about other implicit resources you can reference within SAM
  # https://github.com/awslabs/serverless-application-model/blob/master/docs/internals/generated_resources.rst#api
  GeApiGateway:
    Description: 'API endpoint description'
    Value: !Sub 'https://${GEValidationsApiGateway}.execute-api.${AWS::Region}.amazonaws.com/${AWS::StackName}/validation/'
```
- In order to configure ApiGateway `DomainName` you need to create a new domain in `AWS Route 53`

### Notes:
- _Ref_ returns the value of the specified parameter or resource
- _Fn::Sub_ substitutes variables in an input string with values that you specify.
- _Fn::GetAtt_ intrinsic function returns the value of an attribute from a resource in the template


## HTTP vs RestAPI
https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html
API Gateway WebSocket APIs are bidirectional.