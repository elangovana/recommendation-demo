from elasticsearch_wrapper import createIndex, indexBulkCsv, search
from lambda_elasticsearch_handler import get_es_client


def index_movies_csv(tmp_download_file, esClient):
    # Get ES Client
    indexName = "movies"
    doc_type = "movies"
    createIndex(esClient, indexName)
    delimiter = '|'
    fieldnames = ["_id", "movietitle", "releasedate", "videoreleasedate",
                  "IMDbURL", "unknown", "Action", "Adventure", "Animation",
                  "Childrens", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                  "FilmNoir", "Horror", "Musical", "Mystery", "Romance", "SciFi", "Thriller", "War", "Western"]
    try:
        indexBulkCsv(esClient, indexName,doc_type, tmp_download_file,
                     fieldnames, delimiter)
    except Exception as e:
        print(e)
        raise e



def index_users_csv(tmp_download_file, esClient):
    # Get ES Client
    indexName = "movies"
    doc_type = "users"
    createIndex(esClient, indexName)
    delimiter = '|'
    fieldnames = ["_id", "age" , "gender", "occupation", "zip code"]
    try:
        indexBulkCsv(esClient, indexName,doc_type, tmp_download_file,
                     fieldnames, delimiter)
    except Exception as e:
        print(e)
        raise e


def search_movies_by_title(esClient, movie_search):
    indexName = "movies"
    query = {"match": {"movietitle": movie_search}}
    return search(esClient, indexName, query, 5)