# Swagger to Graphene 
This library can be used to convert Swagger schema into dynamic Graphene models. <br/>
The system can be deloyed on AWS using Serverless framework and can serve GraphQL based queries instantly. 

- Converts swagger models into GraphQL based APIs 
- Dynamic Graphene models 
- Serverless framework for deployment 

### Examples 
---- 
Some examples elaborting the conversion of Swagger Schema into GraphQL API. 

#### 1. Simple Case 
Consider simple swagger schema as specified in [Simple Swagger Definition](https://github.com/amritajain/swagger-graphene/blob/master/data/simple_swagger_definition.json) <br/>
This model is derived from the default PetStore example on [swagger.io](http://swagger.io) and has three fields: id, name, age. <br/>
This library can be used to build dynamic Graphene models, which are then deployed to AWS, making your API ready to be used for GraphQL based queries. <br/>
The image below shows an example of query executed against this simple schema. <br/>
![N|Solid](https://github.com/amritajain/swagger-graphene/blob/master/docs/swagger-graphene-simple-example.png) 

#### 2. Complex Case 
This library is also able to handle complex API schema definitions consisting of varios datatypes such as arrays, nested objects, array of nested objects etc. An example of such schema is defined here [Complex Swagger Definition](https://github.com/amritajain/swagger-graphene/blob/master/data/swagger_definition.json) 

Complex Swagger Schema: 
![N|Solid](https://github.com/amritajain/swagger-graphene/blob/master/docs/swagger-complex-example.png) 

Sample Graphene query: 
![N|Solid](https://github.com/amritajain/swagger-graphene/blob/master/docs/graphene-complex-example.png) 


### Installation 
---- 
**Prerequisites** 
- python 3.6 
- pip3 
- npm 
- AWS account 

**Setup virtual environment** 
```sh 
$ virtualenv -p $(which python3.6) runLocal 
$ source runLocal/bin/activate 
``` 

**Project requirements installations** 
```sh 
$ pip3 install -r requirements.txt 
``` 

**Serverless setup** 
```sh 
$ npm install -g serverless 
$ npm install --save-dev serverless-python-requirements 
``` 

**Setting up source data** 

Open data/databse.csv and edit it to provide the information about your APIs in csv format. 
* Root entity: This would be the root node of GraphQL query or API resource. 
* Swagger souce url: Provide the endpoint for Swagger schema definition. 
* API endpoint: Provide the endpoint for API. (only GETs are supports for now) 

*Sample csv file structure:* 

| Root Entity | Swagger Source Url | API Endpoint | 
| ------------- | ------------- | ------------- | 
| Pet | file:///data/swagger_definition.json | https://github.com/amritajain/swagger-graphene/blob/master/data/api-pet| 


### Deployment
----

Deploy using serverless framework. <br/> You would need AWS's account id and a S3 bucket. 
```sh 
$ (runLocal) serverless deploy --accountID <AWS::AccountId> --stage <dev|qa|prod> --deployment_s3_bucket <s3_bucket_name> 
``` 

*Console Output* 
``` 
>$ (runLocal) serverless deploy --accountID XXX --stage prod --deployment_s3_bucket serverless-bucket-prod-swagger-graphene
>Serverless Warning -------------------------------------- 
>A valid file to satisfy the declaration 'file(serverless.env.yml):prod.env' could not be found. 
>Serverless: Installing required Python packages with python3.6... 
>Serverless: Linking required Python packages... 
>Serverless: Packaging service... 
>Serverless: Unlinking required Python packages... 
>Serverless: Uploading CloudFormation file to S3... 
>Serverless: Uploading artifacts... 
>Serverless: Uploading service .zip file to S3 (24.31 MB)... 
>Serverless: Validating template... 
>Serverless: Creating Stack... 
>Serverless: Checking Stack create progress... 
>................................ 
>Serverless: Stack create finished... 
>Service Information 
>service: swagger-graphene 
>stage: prod 
>region: us-east-1 
>stack: swagger-graphene-prod 
>api keys: 
>   None 
>endpoints: 
>   POST - https://kbey3xz0js.execute-api.us-east-1.amazonaws.com/prod/swagger-graphql 
>functions: 
>   graphqlApp: swagger-graphene-prod-graphqlApp 
``` 

**GraphiQL** 
Use the API gateway url generated as GraphQL Endpoint in GraphiQL to run queries on the API. 
<br/>


### Running Unittests 
---- 
Tests are under tests/unittests folder and can be run using pytest or directly via PyCharm. 
```sh 
$ pytest tests/ 

``` 
<br/>

License 
---- 

MIT 

**Free Software, Hell Yeah!** 
