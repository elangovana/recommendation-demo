from unittest import TestCase
import os
import lambda_sagemaker_handler

class TestLambda_handler(TestCase):

    def test_recommend(self):
        #Please set these variables environment variables before running this set, in your python virtual environment
        #
        # export sagemaker_endpoint="factorization-machines-2018-06-19-06-24-41-438"
        # export elasticsearch_domain_name  = 'your-elastic-search-endpoint.us-east-2.es.amazonaws.com'
        # export AWS_REGION = 'us-east-2'
        # export AWS_ACCESS_KEY_ID = "***"
        # export AWS_SECRET_ACCESS_KEY ="******"
        # export AWS_SESSION_TOKEN =""

        lambda_sagemaker_handler.lambda_handler({
            "params": {"querystring":{"userid":90, "dataset_id":"100KDS"}}
        }, None)
