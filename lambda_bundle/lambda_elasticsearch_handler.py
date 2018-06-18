from __future__ import print_function

import os
import urllib
import uuid

import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth

from elasticsearch_wrapper import connectES, indexBulkCsv, createIndex, search


def index_handler(event, context):
   # Get the object
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
   # Download s3 object
    s3_client = boto3.client('s3')
    tmp_download_file = '/tmp/{}{}'.format(uuid.uuid4(), key)
    s3_client.download_file(bucket, key, tmp_download_file)

    # Get ES Client
    esClient = get_es_client()


    indexName = "movies"
    createIndex(esClient, indexName)

    delimiter = '|'
    fieldnames = ["_id", "movietitle", "releasedate", "videoreleasedate",
                  "IMDbURL", "unknown", "Action", "Adventure", "Animation",
                  "Childrens", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                  "FilmNoir", "Horror", "Musical",  "Mystery", "Romance", "SciFi", "Thriller", "War", "Western"]

    try:
        indexBulkCsv(esClient, indexName, tmp_download_file,
                     fieldnames, delimiter)
    except Exception as e:
        print(e)
        raise e


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
    indexName = "movies"
    query = {"match": {"movietitle": movie_search}}

    return search(esClient, indexName, query, 5)
