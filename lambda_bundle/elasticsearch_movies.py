from elasticsearch_wrapper import createIndex, indexBulkCsv, search

import config


def index_csv(tmp_download_file, esClient, dataset_id, doc_type):
    # Get ES Client
    indexName = get_index(dataset_id)
    createIndex(esClient, indexName)
    delimiter = config.DataSet[dataset_id][doc_type][config.DELIMITER]
    fieldnames = config.DataSet[dataset_id][doc_type][config.CSVFIELD_NAMES]
    try:
        indexBulkCsv(esClient, indexName, doc_type, tmp_download_file,
                     fieldnames, delimiter)
    except Exception as e:
        print(e)
        raise e


def search_movies_by_title(esClient, movie_search, dataset_id):
    indexName = get_index(dataset_id)
    query = {"match": {"movietitle": movie_search}}
    return search(esClient, indexName, query, {}, 5)


def get_user_by_id(esClient, userid, dataset_id):
    indexName = get_index(dataset_id)
    query = {"ids": {
        "type": config.DOCTYPE_USERS,
        "values": [userid]
    }}
    user_search_result = search(esClient, indexName, query, {}, 1)

    userid = user_search_result["hits"]["hits"][0]["_id"]
    user = user_search_result["hits"]["hits"][0]["_source"]

    # get ratings for user
    ratings_query = {
        "bool": {
            "should": [
                {"match": {"_type": config.DOCTYPE_RATINGS}},
                {"match": {"userid": userid}}
            ]
        }
    }
    rating_sort = {config.RATINGS_FIELD_RATING: "desc"}
    search_ratings_result = search(esClient, indexName, ratings_query, rating_sort, 50)["hits"]["hits"]

    movie_id_rating_dict = {}
    for h in search_ratings_result:
        movie_id_rating_dict[h["_source"][config.RATINGS_FIELD_MOVIEID]] = h["_source"][config.RATINGS_FIELD_RATING]

    # Get movies
    movie_query = {
        "ids": {
            "type": config.DOCTYPE_MOVIES,
            "values": list(movie_id_rating_dict.keys())
        }

    }
    search_movies_result = search(esClient, indexName, movie_query, {}, 50)["hits"]["hits"]

    ratings = []
    for moviehit in search_movies_result:
        ratings.append({
            "movie_title": moviehit["_source"][config.MOVIES_FIELD_TITLE]
            , "movie_release_date": moviehit["_source"][config.MOVIES_FIELD_RELEASEDATE]
            , "movie_id": moviehit["_id"]
            , "rating": movie_id_rating_dict[moviehit["_id"]]
        })
        # ratings.append({
        #     "movieid":hit["_source"][config.RATINGS_FIELD_MOVIEID]
        #     ,"rating":hit["_source"][config.RATINGS_FIELD_RATING]
        # })

    # Consolidate results

    result = {"user": {
        "id": userid
        , "age": user[config.USER_FIELD_AGE]
        , "occupation": user[config.USER_FIELD_OCCUPATION]
        , "gender": user[config.USER_FIELD_GENDER]
    },
        "ratings": ratings}

    return result


def get_index(dataset_id):
    indexName = config.DataSet[dataset_id][config.INDEXNAME]
    return indexName
