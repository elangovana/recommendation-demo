from __future__ import print_function

import os
import tempfile
import urllib
import uuid

import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth

from elasticsearch_movies import  search_movies_by_title,  get_user_by_id, index_csv
from elasticsearch_wrapper import connectES
import random
import config

def index_handler(event, context):
   # Get the object
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    #get Meta data
    s3_client = boto3.client('s3')
    response = s3_client.head_object(Bucket=bucket, Key=key)
    dataset_id = response['Metadata']['dataset_id']
    type = response['Metadata']['type']


   # Download s3 object
    tmpdir=tempfile.mkdtemp(prefix="test")
    tmp_download_file = '{}/{}.csv'.format(tmpdir, uuid.uuid4())
    s3_client.download_file(bucket, key, tmp_download_file)

    #Index
    esClient = _get_es_client()
    index_csv(tmp_download_file, esClient, dataset_id, type)



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
    movie_search = event["params"]["querystring"]["movie"]
    dataset_id = event["params"]["querystring"]["dataset_id"]
    esClient = _get_es_client()
    return search_movies_by_title(esClient, movie_search, dataset_id)


def get_datasets_handler(event, context):
    result = []
    for key in config.DataSet.keys():
        result.append({"id": key, "description": config.DataSet[key][config.DATASET_DESCRIPTION]})
    return result

def get_random_user_handler(event, context):
    dataset_id = event["params"]["querystring"]["dataset_id"]
    nb_users = config.DataSet[dataset_id][config.NB_USERS]
    random_user_id = random.randint(1, nb_users)
    esClient = _get_es_client()
    result = get_user_by_id(esClient, random_user_id, dataset_id)

    return result
