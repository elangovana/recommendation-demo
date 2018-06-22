from __future__ import print_function

import os
import urllib
import uuid

import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth

from elasticsearch_movies import index_movies_csv, search_movies_by_title, index_users_csv, get_user_by_id
from elasticsearch_wrapper import connectES
import random
import config

def index_movies_handler(event, context):
   # Get the object
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    #get Meta data
    s3_client = boto3.client('s3')
    response = s3_client.head_object(Bucket=bucket, Key=key)
    dataset_id = response['Metadata']['dataset_id']


   # Download s3 object
    tmp_download_file = '/tmp/{}{}'.format(uuid.uuid4(), key)
    s3_client.download_file(bucket, key, tmp_download_file)

    #Index movies
    esClient = _get_es_client()
    index_movies_csv(tmp_download_file, esClient, dataset_id)

def index_users_handler(event, context):
   # Get the object
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])


    # get Meta data
    s3_client = boto3.client('s3')
    response = s3_client.head_object(Bucket=bucket, Key=key)
    dataset_id = response['Metadata']['dataset']

   # Download s3 object
    tmp_download_file = '/tmp/{}{}'.format(uuid.uuid4(), key)
    s3_client.download_file(bucket, key, tmp_download_file)

    #Index movies
    esClient = _get_es_client()
    index_users_csv(tmp_download_file, esClient,  dataset_id)

def _get_es_client():
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
    movie_search = event["querystring"]["movie"]
    dataset_id = event["querystring"]["dataset_id"]
    esClient = _get_es_client()
    return search_movies_by_title(esClient, movie_search, dataset_id)



def get_random_user_handler(event, context):
    dataset_id = event["querystring"]["dataset_id"]
    random_user_id = random.randint(1, config.DataSet[dataset_id].nbusers)
    esClient = _get_es_client()
    return get_user_by_id(esClient, random_user_id, dataset_id)
