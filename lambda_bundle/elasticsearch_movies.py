from elasticsearch_wrapper import createIndex, indexBulkCsv, search


import config

def index_csv(tmp_download_file, esClient, dataset_id, doc_type):
    # Get ES Client
    indexName = get_index(dataset_id)
    createIndex(esClient, indexName)
    delimiter =  config.DataSet[dataset_id][config.DELIMITER]
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
    return search(esClient, indexName, query, 5)


def get_user_by_id(esClient, id, dataset_id):
    indexName = get_index(dataset_id)
    query = {"ids": {
        "type": config.DOCTYPE_USERS,
        "values": [id]
    }}
    user = search(esClient, indexName, query, 1)["hits"]["hits"]["_source"]
    # ratings_query= {"userid": {
    #     "type": config.DOCTYPE_RATINGS,
    #     "values": [user.]
    # }}

    result = {user: {
        "age": user[config.USER_FIELD_AGE],
        "occupation": user[config.USER_FIELD_OCCUPATION],
        "gender": user[config.USER_FIELD_GENDER]
    }}
    return result


def get_index(dataset_id):
    indexName = config.DataSet[dataset_id][config.INDEXNAME]
    return indexName
