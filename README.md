# recommendation-demo
SageMaker recommendation engine demo

# Build
1. Create a codepipeline stack using codebuild_cloudformation.json
2. Build on code build buildspec.yml (use python 3.6 runtime). This spec creates the following artifacts
  * Cloudformation template
  * webapp
  * lambda code
3. Download the zip of webapp  to your local file system and extract them.
4. Upload the webfiles to your destination s3 bucket to serve as the content origin
```shell
aws s3 cp --recursive ~/Downloads/webapp/ s3://<yourbucket>/webapp
```
# Public Datasets set up
1. Download movies
```shell
wget http://files.grouplens.org/datasets/movielens/ml-100k/u.item
aws s3 cp u.item s3://<yourbucketData>/movies.csv
```


# Run
1. Deploy CFN
```shell
aws cloudformation create-stack  --stack-name RecommeddationDemo --template-url https://s3.amazonaws.com/aegovan-builds/Cloudformation.json --capabilities CAPABILITY_NAMED_IAM --parameters ParameterKey="elasticSearchDomainName",ParameterValue="movies" ParameterKey="s3BucketData",ParameterValue="aegovanmoviesdata" ParameterKey="lambdaElasticSearchIndexFunctionName",ParameterValue="indexElasticSearch" ParameterKey="s3BucketData",ParameterValue="aegovanmoviesdatasset" ParameterKey="s3BucketLambdaCode",ParameterValue="aegovan-builds" ParameterKey="s3BucketLambdacodeElasticSearchIndex",ParameterValue="lambda_bundle.zip" ParameterKey="s3BucketNameWebApp",ParameterValue="aegovan-builds.s3.amazonaws.com" ParameterKey="s3BucketNameWebAppKey",ParameterValue="/webapp" 

```


# Test
1. Lambda ES index test, using sample data as 
```json
{
  "Records": [
    {
      
      
      "s3": {
      
        "object": {
          "key": "movies.csv"
        },
        "bucket": {
          "name": "<your-bucket-containing-movies.csv>"
        }
    
      }
    }
  ]
}
```