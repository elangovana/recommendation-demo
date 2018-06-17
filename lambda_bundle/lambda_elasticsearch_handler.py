from __future__ import print_function
from pprint import pprint
import boto3
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection

import urllib
import json
import os
from elasticsearch_wrapper import connectES, indexBulkCsv, createIndex, search
from aws_requests_auth.aws_auth import AWSRequestsAuth


def index_handler(event, context):
    esdomain = os.environ['elasticsearch_domain_name']
    auth = AWSRequestsAuth(aws_access_key=os.environ['AWS_ACCESS_KEY_ID'],
                           aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                           aws_token=os.environ['AWS_SESSION_TOKEN'],
                           aws_host=esdomain,
                           aws_region='us-east-1',
                           aws_service='es')

    esClient = connectES(esdomain, auth)
    indexName = "movies"
    createIndex(esClient, indexName)

    delimiter = '|'
    fieldnames = ["_id", "movietitle", "releasedate", "videoreleasedate",
                  "IMDbURL", "unknown", "Action", "Adventure", "Animation",
                  "Childrens", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                  "FilmNoir", "Horror", "Musical",  "Mystery", "Romance", "SciFi", "Thriller", "War", "Western"]

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    try:
        indexBulkCsv(esClient, indexName, bucket, key, fieldnames, delimiter)
    except Exception as e:
        print(e)
        raise e


def search_movies_handler(event, context):
    esdomain = os.environ['elasticsearch_domain_name']
    auth = AWSRequestsAuth(aws_access_key=os.environ['AWS_ACCESS_KEY_ID'],
                           aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                           aws_token=os.environ['AWS_SESSION_TOKEN'],
                           aws_host=esdomain,
                           aws_region='us-east-1',
                           aws_service='es')
    movie_search = event["queryStringParameters"]["movie"]
    esClient = connectES(esdomain, auth)
    indexName = "movies"
    query = {{"match": {"movietitle": movie_search}}}

    return search(esClient, indexName, query, 5)
    
