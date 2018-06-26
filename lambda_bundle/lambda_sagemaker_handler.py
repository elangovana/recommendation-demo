import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth
from scipy.sparse import lil_matrix
import json
import os

import config
from elasticsearch_movies import search_ratings_by_userid, search_movies_by_ids
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

    print(seenMovieList)

    # remove seen movies
    newMovieList = [m for m in range(1, config.DataSet[dataset_id][config.NB_MOVIES])  if not str(m) in seenMovieList ]
    # get movie details
    movies_search = search_movies_by_ids(esclient, indexName, newMovieList)
    movie_dict = {}
    for m in movies_search:
        movie_dict[m["_id"]] = {"movie_title": m["_source"][config.MOVIES_FIELD_TITLE],
                                "movie_release_date": m["_source"][config.MOVIES_FIELD_RELEASEDATE]}



    # prepare matrix
    print(newMovieList)
    print(len(newMovieList))
    matrix = convert_to_matrix(newMovieList, dataset_id, user_id)



    #predictions for unseen movies
    result = []
    i =0;
    for recommeded_list in invoke_sagemaker(endpoint, matrix):
        for movie in recommeded_list:
            if int(movie["predicted_label"]) == 0: continue
            result.append({"movieid": newMovieList[i],
                           "movie_details": movie_dict[str(newMovieList[i])],
                           "like": movie["predicted_label"],
                           "score": movie["score"]})
            i = i + 1



    #sort by prediction score
    result.sort(key=lambda x: x["score"], reverse=True)

    return result


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
    data_array = cooMatrix.toarray()
    batch_size = 100
    result = []
    for i in range(0, len(data_array), batch_size):

        json_data = fm_serializer(data_array[i:i+batch_size])
        response = client.invoke_endpoint(
            EndpointName=endpoint,
            Body=json_data,
            ContentType='application/json'
        )

        string_data = json.loads( response["Body"].read().decode("utf-8"))
        result.extend(string_data["predictions"])
        yield string_data["predictions"]
        print(string_data)
    print(len(result))
    return result


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
