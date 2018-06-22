from __future__ import print_function

import os
import urllib
import uuid

import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth

from elasticsearch_movies import index_movies_csv, search_movies_by_title, index_users_csv, get_user_by_id
from elasticsearch_wrapper import connectES
import random

def index_movies_handler(event, context):
   # Get the object
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
   # Download s3 object
    s3_client = boto3.client('s3')
    tmp_download_file = '/tmp/{}{}'.format(uuid.uuid4(), key)
    s3_client.download_file(bucket, key, tmp_download_file)

    #Index movies
    esClient = _get_es_client()
    index_movies_csv(tmp_download_file, esClient)

def index_users_handler(event, context):
   # Get the object
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
   # Download s3 object
    s3_client = boto3.client('s3')
    tmp_download_file = '/tmp/{}{}'.format(uuid.uuid4(), key)
    s3_client.download_file(bucket, key, tmp_download_file)

    #Index movies
    esClient = _get_es_client()
    index_users_csv(tmp_download_file, esClient)

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
    esClient = _get_es_client()
    return search_movies_by_title(esClient, movie_search)



def get_random_user_handler(event, context):
    # TODO Too bad this is hardcoded!!. Needs to be aligned with the no:of features in the movies dataset, which is no_users + no_nmovies
    nbUsers = 943
    nbMovies = 1682
    random_user_id = random.randint(1, nbUsers)
    esClient = _get_es_client()
    return get_user_by_id(esClient, random_user_id)
