import logging

import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth
from scipy.sparse import lil_matrix
import json
import os
from sagemaker.amazon.common import  write_spmatrix_to_sparse_tensor
import io
import config
from elasticsearch_movies import search_ratings_by_userid, search_movies_by_ids
from elasticsearch_wrapper import connectES


def lambda_handler(event, context):
    # TODO implement
    user_id = event["params"]["querystring"]["userid"]
    dataset_id = event["params"]["querystring"]["dataset_id"]
    endpoint = os.environ['sagemaker_endpoint_{}'.format(dataset_id)]
    # Get movies that user has seen
    esclient = _get_es_client()
    indexName = config.DataSet[dataset_id][config.INDEXNAME]
    seenMovieList = [h["_source"][config.RATINGS_FIELD_MOVIEID] for h in
                     search_ratings_by_userid(esclient, indexName, user_id)]



    # remove seen movies
    newMovieList = [m for m in range(1, config.DataSet[dataset_id][config.NB_MOVIES])  if not str(m) in seenMovieList ]
    # get movie details
    movies_search = search_movies_by_ids(esclient, indexName, newMovieList)
    movie_dict = {}
    for m in movies_search:
        movie_dict[m["_id"]] = {"movie_title": m["_source"][config.MOVIES_FIELD_TITLE],
                                "movie_release_date": m["_source"][config.MOVIES_FIELD_RELEASEDATE]}



    # prepare matrix

    matrix = convert_to_matrix(newMovieList, dataset_id, user_id)



    #predictions for unseen movies
    result = []
    i =0;
    min_confidence_score = 0.8
    for recommeded_list in invoke_sagemaker(endpoint, matrix):
        for movie in recommeded_list:
            if (movie["score"]) < min_confidence_score: continue
            result.append({"movieid": newMovieList[i],
                           "movie_details": movie_dict[str(newMovieList[i])],
                           "like": movie["predicted_label"],
                           "score": movie["score"]})
            i = i + 1



    #sort by prediction score
    result.sort(key=lambda x: x["score"], reverse=True)

    return result[1:30]


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
    logger = logging.getLogger(__name__)
    client = boto3.client('runtime.sagemaker')

    yield from recordio_load(client, cooMatrix, endpoint, logger)


def jsonformat_load(client, cooMatrix, endpoint, logger):
    logger = logging.getLogger(__name__)

    data_array = cooMatrix.toarray()
    batch_size = 250

    for i in range(0, len(data_array), batch_size):
        logger.info("Converting to recordio matrix from rows  {} to {} ".format(i, i + batch_size))
        content_type, data = fm_serializer(data_array[i:i + batch_size])
        logger.info("Invoking sagemaker from  rows {} to {} data".format(i, i + batch_size))
        response = client.invoke_endpoint(
            EndpointName=endpoint,
            Body=data,
            ContentType=content_type
        )
        string_data = json.loads(response["Body"].read().decode("utf-8"))
        logger.info("Received predictions from sagemaker\n{}".format(string_data))
        yield string_data["predictions"]


def recordio_load(client, cooMatrix, endpoint, logger):
        logger = logging.getLogger(__name__)
        data_array = cooMatrix


        logger.info("Converting to recordio matrix from rows ".format())
        content_type, data = recordio_serialiser(data_array)
        logger.info("Invoking sagemaker ".format())
        response = client.invoke_endpoint(
            EndpointName=endpoint,
            Body=data,
            ContentType=content_type
        )

        string_data = json.loads(response["Body"].read().decode("utf-8"))
        logger.debug("Received predictions from sagemaker\n{}".format(string_data))
        yield string_data["predictions"]


def fm_serializer(data):
    js = {'instances': []}
    for row in data:
        js['instances'].append({'features': row.tolist()})
    return ('application/json',json.dumps(js))

def recordio_serialiser(data):
    buf = io.BytesIO()
    write_spmatrix_to_sparse_tensor(buf, data)
    buf.seek(0)
    return ("application/x-recordio-protobuf", buf)

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
