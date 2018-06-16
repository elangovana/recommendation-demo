from __future__ import print_function
from pprint import pprint
import boto3
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection

import urllib
import json
import os
from elasticsearch_wrapper import connectES, indexBulkCsv, createIndex
from aws_requests_auth.aws_auth import AWSRequestsAuth


def index_handler(event, context):
    esdomain = os.environ['elasticsearch_domain_name']
    auth = AWSRequestsAuth(aws_access_key=os.environ['AWS_ACCESS_KEY_ID'],
                           aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                           aws_token=esdomain,
                           aws_host=esClient,
                           aws_region='us-east-1',
                           aws_service='es')

    esClient = connectES(esdomain, auth)
    indexName = "movies"
    createIndex(esClient, indexName)

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(
        event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        indexBulkCsv(esClient, indexName, bucket, key)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
