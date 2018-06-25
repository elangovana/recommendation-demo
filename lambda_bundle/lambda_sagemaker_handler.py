import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth
from scipy.sparse import lil_matrix
import json
import os

import config
from elasticsearch_movies import search_ratings_by_userid
from elasticsearch_wrapper import connectES


def lambda_handler(event, context):
    # TODO implement
    endpoint = os.environ['sagemaker_endpoint']
    user_id = event["params"]["querystring"]["userid"]
    dataset_id = event["params"]["querystring"]["dataset_id"]

    # Get movies that user has seen
    esclient = _get_es_client()
    indexName = config.DataSet[dataset_id][config.INDEXNAME]
    seenMovieList = [h["_source"][config.RATINGS_FIELD_MOVIEID] for h in
                     search_ratings_by_userid(esclient, indexName, user_id)]

    # remove seen movies
    newMovieList = [m for m in seenMovieList if not m in range(1, config.DataSet[dataset_id][config.NB_MOVIES])]
    matrix = convert_to_matrix(newMovieList, dataset_id, user_id)

    recommeded_list = invoke_sagemaker(endpoint, matrix)
    print(recommeded_list)
    result = []
    for i in range(0, len(newMovieList)):
        #if recommeded_list[i] == 0 : continue
        result.append({"movieid":newMovieList[i],"like":recommeded_list[i], "score": recommeded_list[i]})

    return recommeded_list


def convert_to_matrix(moviesList, dataset_id, user_id):
    nbUsers = config.DataSet[dataset_id][config.NB_USERS]
    nbMovies = config.DataSet[dataset_id][config.NB_MOVIES]

    nbFeatures = nbUsers + nbMovies
    nbRatings = len(moviesList)
    X = lil_matrix((nbRatings, nbFeatures), dtype='float32')

    line = 0

    for movieId in moviesList:
        X[line, int(user_id) - 1] = 1
        X[line, int(nbUsers) + int(movieId) - 1] = 1
        line = line + 1

    return X


def invoke_sagemaker(endpoint, cooMatrix):
    client = boto3.client('runtime.sagemaker')
    json_data = fm_serializer(cooMatrix.toarray())
    response = client.invoke_endpoint(
        EndpointName=endpoint,
        Body=json_data,
        ContentType='application/json'
    )

    string_data = response["Body"].read().decode("utf-8")
    return string_data


def fm_serializer(data):
    js = {'instances': []}
    for row in data:
        js['instances'].append({'features': row.tolist()})
    return json.dumps(js)


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
