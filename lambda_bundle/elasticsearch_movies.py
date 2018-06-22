from elasticsearch_wrapper import createIndex, indexBulkCsv, search

doc_type_user = "users"
import config

def index_movies_csv(tmp_download_file, esClient, dataset_id):
    # Get ES Client
    indexName = get_index(dataset_id)
    doc_type = "movies"
    createIndex(esClient, indexName)
    delimiter = '|'
    fieldnames = config.DataSet[dataset_id].moviedatasetfields
    try:
        indexBulkCsv(esClient, indexName, doc_type, tmp_download_file,
                     fieldnames, delimiter)
    except Exception as e:
        print(e)
        raise e


def index_users_csv(tmp_download_file, esClient, dataset_id):
    # Get ES Client
    indexName = get_index(dataset_id)

    createIndex(esClient, indexName)
    delimiter = '|'
    fieldnames = config.DataSet[dataset_id].userdatasetfields
    try:
        indexBulkCsv(esClient, indexName, doc_type_user, tmp_download_file,
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
        "type": doc_type_user,
        "values": [id]
    }}
    return search(esClient, indexName, query, 5)


def get_index(dataset_id):
    indexName = "movies_{}".format(dataset_id)
    return indexName
