from __future__ import print_function
from pprint import pprint
import boto3
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection

import urllib
import json
import os
from es_index import connectES,indexDocElement

def lambda_handler(event, context):
   esClient = connectES(os.environ['elasticsearch_domain_name'])
   createIndex(esClient)

   # Get the object from the event and show its content type
   bucket = event['Records'][0]['s3']['bucket']['name']
   key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
   try:
     response = s3.get_object(Bucket=bucket, Key=key)
     print(response)
     print("KEY: " + key)
     print("CONTENT TYPE: " + response['ContentType'])
     print("Metadata : " + json.dumps(response['Metadata']))
     print("Custom 1: " + response['ResponseMetadata']['HTTPHeaders']['x-amz-meta-custom1'])
     print("Custom 2: " + response['ResponseMetadata']['HTTPHeaders']['x-amz-meta-custom2'])
     indexDocElement(esClient,key,response)
     return response['ContentType']
   except Exception as e:
     print(e)
     print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
     raise e