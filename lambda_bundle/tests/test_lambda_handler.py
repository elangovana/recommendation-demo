from unittest import TestCase
import os
import lambda_sagemaker_handler

class TestLambda_handler(TestCase):

    def test_recommend(self):
        # os.environ['sagemaker_endpoint']="factorization-machines-2018-06-19-06-24-41-438"
        # os.environ['elasticsearch_domain_name'] = 'search-movies-rriuwfsv6q45i6ltiaidxbafky.us-east-2.es.amazonaws.com'
        # os.environ['AWS_REGION'] = 'us-east-2'
        #
        # os.environ['AWS_ACCESS_KEY_ID'] = "***"
        # os.environ['AWS_SECRET_ACCESS_KEY']="******"
        # os.environ['AWS_SESSION_TOKEN']=""

        lambda_sagemaker_handler.lambda_handler({
            "params": {"querystring":{"userid":90, "dataset_id":"100KDS"}}
        }, None)
