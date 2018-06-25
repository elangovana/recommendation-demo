from elasticsearch_wrapper import createIndex, indexBulkCsv, search


import config

def index_csv(tmp_download_file, esClient, dataset_id, doc_type):
    # Get ES Client
    indexName = get_index(dataset_id)
    createIndex(esClient, indexName)
    delimiter =  config.DataSet[dataset_id][doc_type][config.DELIMITER]
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
    return search(esClient, indexName, query,{}, 5)


def get_user_by_id(esClient, userid, dataset_id):
    indexName = get_index(dataset_id)
    query = {"ids": {
        "type": config.DOCTYPE_USERS,
        "values": [userid]
    }}
    user_search_result = search(esClient, indexName, query,{}, 1)

    userid = user_search_result["hits"]["hits"][0]["_id"]
    user = user_search_result["hits"]["hits"][0]["_source"]

    #get ratings for user
    ratings_query= {
        "bool": {
            "should": [
              { "match": { "_type":  config.DOCTYPE_RATINGS }},
              { "match": { "userid": userid  }}
            ]
          }
    }
    rating_sort ={config.RATINGS_FIELD_RATING:"desc"}

    user_search_ratings_result = search(esClient, indexName, ratings_query, rating_sort, 50)["hits"]["hits"]
    ratings =[]
    movie_ids =[]
    for hit in user_search_ratings_result:
        movie_ids.append(hit["_source"][config.RATINGS_FIELD_MOVIEID])
        ratings.append({
            "movieid":hit["_source"][config.RATINGS_FIELD_MOVIEID]
            ,"rating":hit["_source"][config.RATINGS_FIELD_RATING]
        })


    result = {"user": {
        "id":userid
       , "age": user[config.USER_FIELD_AGE]
       , "occupation": user[config.USER_FIELD_OCCUPATION]
       , "gender": user[config.USER_FIELD_GENDER]
    },
    "ratings":ratings}


    return result


def get_index(dataset_id):
    indexName = config.DataSet[dataset_id][config.INDEXNAME]
    return indexName
