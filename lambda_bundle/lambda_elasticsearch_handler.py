from __future__ import print_function

import os
import urllib
import uuid

import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth

from elasticsearch_movies import index_movies_csv, search_movies_by_title
from elasticsearch_wrapper import connectES


def index_handler(event, context):
   # Get the object
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
   # Download s3 object
    s3_client = boto3.client('s3')
    tmp_download_file = '/tmp/{}{}'.format(uuid.uuid4(), key)
    s3_client.download_file(bucket, key, tmp_download_file)

    #Index movies
    esClient = get_es_client()
    index_movies_csv(tmp_download_file, esClient)


def get_es_client():
    # es
    esdomain = os.environ['elasticsearch_domain_name']
    region = os.environ['AWS_REGION']
    print(region)
    auth = AWSRequestsAuth(aws_access_key=os.environ['AWS_ACCESS_KEY_ID'],
                           aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                           aws_token=os.environ['AWS_SESSION_TOKEN'],
                           aws_host=esdomain,
                           aws_region=region,
                           aws_service='es')
    esClient = connectES(esdomain, auth)
    return esClient


def search_movies_handler(event, context):
    movie_search = event["queryStringParameters"]["movie"]
    esClient = get_es_client()
    return search_movies_by_title(esClient, movie_search)


