from __future__ import print_function
from pprint import pprint
import boto3
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection

import urllib
import json


def connectES(esEndPoint):
 print ('Connecting to the ES Endpoint {0}'.format(esEndPoint))
 try:
  esClient = Elasticsearch(
   hosts=[{'host': esEndPoint, 'port': 443}],
   use_ssl=True,
   verify_certs=True,
   connection_class=RequestsHttpConnection)
  return esClient
 except Exception as E:
  print("Unable to connect to {0}".format(esEndPoint))
  print(E)
  exit(3)




def createIndex(esClient):
 try:
  res = esClient.indices.exists('metadata-store')
  print("Index Exists ... {}".format(res))
  if res is False:
   esClient.indices.create('metadata-store', body=indexDoc)
   return 1
 except Exception as E:
  print("Unable to Create Index {0}".format("metadata-store"))
  print(E)
  exit(4)

def indexDocElement(esClient, key, response):
  try:
   indexObjectKey = key
   indexcreatedDate = response['LastModified']
   indexcontent_length = response['ContentLength']
   indexcontent_type = response['ContentType']
   indexmetadata = json.dumps(response['Metadata'])
   retval = esClient.index(index='metadata-store', doc_type='images', body={
     'createdDate': indexcreatedDate,
     'objectKey': indexObjectKey,
     'content_type': indexcontent_type,
     'content_length': indexcontent_length,
     'metadata': indexmetadata
   })
  except Exception as E:
    print("Doc not indexed")
    print("Error: ",E)
    exit(5)