# Recommendation Demo
SageMaker recommendation engine demo

# Set up Sagemaker matrix factorisation
1. On AWS SageMaker Console launch a new notebook instance.
2. Run the python notebook sagemaker/factorisation_machines.ipynb. Please note this notebook is sourced from  https://gitlab.com/juliensimon/dlnotebooks. 
3. Deploy the sagemaker endpoint. This is required to launch the cloudformation web app stack.


# Download Public Datasets
We use the MovieLens dataset.

F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets:
History and Context. ACM Transactions on Interactive Intelligent
Systems (TiiS) 5, 4, Article 19 (December 2015), 19 pages.
DOI=http://dx.doi.org/10.1145/2827872


## 100K Movie Dataset
1. Download movies
```shell
wget http://files.grouplens.org/datasets/movielens/ml-100k/u.item
aws s3 cp u.item s3://<yourbucketData>/movies.csv --metadata dataset_id=100KDS,type=movies
```
2. Download users
```shell
wget http://files.grouplens.org/datasets/movielens/ml-100k/u.user
aws s3 cp u.user s3://<yourbucketData>/users.csv --metadata dataset_id=100KDS,type=users
```

3. Download ratings
```shell
wget http://files.grouplens.org/datasets/movielens/ml-100k/u.data
aws s3 cp u.data s3://<yourbucketData>/ratings.csv --metadata dataset_id=100KDS,type=ratings
```


# Build the web app
1. Create a codepipeline stack using codebuild_cloudformation.json
2. Start a build on codepipeline. This should upload the following artifacts in the s3 bucket you specified in the codepipeline stack
  * Cloudformation template
  * webapp
  * lambda code
3. Download the zip of webapp  to your local file system and extract them.
4. Upload the webfiles to your destination s3 bucket to serve as the content origin
```shell
aws s3 cp --recursive ~/Downloads/webapp/ s3://<yourbucket>/webapp
```

# Run
1. Deploy cloudformation stack using ./apigateway_lambda_sam.yaml
[[https://github.com/elangovana/recommendation-demo/raw/master/docs/Recommendation%20Engine%20Web%20App.png]]
<!-- ```shell
aws cloudformation create-stack  --stack-name RecommeddationDemo --template-url https://s3.amazonaws.com/aegovan-builds/Cloudformation.json --capabilities CAPABILITY_NAMED_IAM --parameters ParameterKey="elasticSearchDomainName",ParameterValue="movies" ParameterKey="s3BucketData",ParameterValue="aegovanmoviesdata" ParameterKey="lambdaElasticSearchIndexFunctionName",ParameterValue="indexElasticSearch"  ParameterKey="s3BucketLambdaCode",ParameterValue="aegovan-builds" ParameterKey="s3BucketLambdacodeElasticSearchIndex",ParameterValue="lambda_bundle.zip" ParameterKey="s3BucketNameWebApp",ParameterValue="aegovan-builds.s3.amazonaws.com" ParameterKey="s3BucketNameWebAppKey",ParameterValue="/webapp" 

``` -->


# Load Elastic seach movies data
1. Make sure you that you have metadata "dataset_id" set on the key you want to index to either 100KDS, 20MDS to represent the 2 different data set

2. Load movies into elastic search
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

3. Load users into elastic search
```json
{
  "Records": [
    {
      
      
      "s3": {
      
        "object": {
          "key": "users.csv"
        },
        "bucket": {
          "name": "<your-bucket-containing-movies.csv>"
        }
    
      }
    }
  ]
}
```

4. Load user ratings into elastic search
```json
{
  "Records": [
    {
      
      
      "s3": {
      
        "object": {
          "key": "rating.csv"
        },
        "bucket": {
          "name": "<your-bucket-containing-movies.csv>"
        }
    
      }
    }
  ]
}
```

# Web app
Your recommendation engine web app is now ready to use, the url is the output of the cloudformation.

