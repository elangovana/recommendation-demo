import tempfile
from unittest import TestCase

import os
from ddt import ddt, data, unpack
import boto3
import config
from lambda_elasticsearch_handler import index_handler
import urllib.request

'''
Prerequistes.. This is an integration test. Requires the Elastic search environment to be set up. 
Make sure the following environment variables are available
        
        # export elasticsearch_domain_name  = 'your-elastic-search-endpoint.us-east-2.es.amazonaws.com'
        # export AWS_REGION = 'us-east-2'
        # export AWS_ACCESS_KEY_ID = "***"
        # export AWS_SECRET_ACCESS_KEY ="******"
        # export AWS_SESSION_TOKEN =""
        # export TEST_VAR_BUCKET ="<myBucketForData>"
'''


@ddt
class TestItElasticSearchHandler(TestCase):

    @data(
        (config.DATASETID_100K, config.DOCTYPE_MOVIES, "http://files.grouplens.org/datasets/movielens/ml-100k/u.item",
         "tmp")
    , (config.DATASETID_100K, config.DOCTYPE_USERS, "http://files.grouplens.org/datasets/movielens/ml-100k/u.user",
         "tmp"))
    @unpack
    def test_recommend(self, dataset_id, doc_type, url, bucket_key):
        # Arrange
        response = urllib.request.urlopen(url).read()
        bucket = os.environ['TEST_VAR_BUCKET']
        #with tempfile.TemporaryFile() as tmpfile:
        key = self.upload_file_to_s3(response, bucket, bucket_key, dataset_id, doc_type)

        # Act
        index_handler({
            "Records": [
                {

                    "s3": {

                        "object": {
                            "key": key
                        },
                        "bucket": {
                            "name": bucket
                        }

                    }
                }
            ]
        }
            , None)

    def upload_file_to_s3(self, local_file, bucket, bucket_key, dataset_id, doc_type):
        client = boto3.client('s3')

        s3ObjectKey = "{}/{}_{}.csv".format(bucket_key, dataset_id, doc_type)
        client.put_object(Body=local_file, Bucket=bucket, Key=s3ObjectKey, ContentType="text/csv", Metadata={
            "dataset_id": dataset_id,
            "type": doc_type

        }, StorageClass="REDUCED_REDUNDANCY", ContentEncoding=config.DataSet[dataset_id]["Encoding"])

        return s3ObjectKey
