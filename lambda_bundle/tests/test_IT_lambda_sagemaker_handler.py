from unittest import TestCase
import os

import config
import lambda_sagemaker_handler

'''
Prerequistes.. This is an integration test. Requires the Elastic search & SageMaker environment to be set up. 
Make sure the following environment variables are available
        # export sagemaker_endpoint_100KDS="factorization-machines-2018-06-19-06-24-41-438"
        # export elasticsearch_domain_name  = 'your-elastic-search-endpoint.us-east-2.es.amazonaws.com'
        # export AWS_REGION = 'us-east-2'
        # export AWS_ACCESS_KEY_ID = "**************"
        # export AWS_SECRET_ACCESS_KEY ="******"
        # export AWS_SESSION_TOKEN ="" 
'''


class TestItLambdaSageMakerHandler(TestCase):

    def test_recommend(self):
        lambda_sagemaker_handler.lambda_handler({
            "params": {"querystring":
                           {"userid": 90,
                            "dataset_id": config.DATASETID_100K}
                       }
        }
            , None)
