# recommendation-demo
SageMaker recommendation engine demo

# Run
1. Deploy CFN
```shell
aws cloudformation create-stack  --stack-name RecommeddationDemo --template-url https://s3.amazonaws.com/aegovan-builds/Cloudformation.json --capabilities CAPABILITY_NAMED_IAM --parameters ParameterKey="elasticSearchDomainName",ParameterValue="movies" ParameterKey="s3BucketData",ParameterValue="aegovanmoviesdata" ParameterKey="lambdaElasticSearchIndexFunctionName",ParameterValue="indexElasticSearch" ParameterKey="s3BucketData",ParameterValue="aegovanmoviesdatasset" ParameterKey="s3BucketLambdaCode",ParameterValue="aegovan-builds" ParameterKey="s3BucketLambdacodeElasticSearchIndex",ParameterValue="lambda_bundle.zip" ParameterKey="s3BucketNameWebApp",ParameterValue="aegovan-builds.s3.amazonaws.com" ParameterKey="s3BucketNameWebAppKey",ParameterValue="/webapp" 

```
