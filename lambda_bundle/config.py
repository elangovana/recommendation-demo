DATASETID_100K = "100KDS"
DOCTYPE_MOVIES ="movies"
DOCTYPE_USERS="users"
CSVFIELD_NAMES="fieldnames"

DataSet = {
    DATASETID_100K: {"name": "100K Data set", "nbusers": 943, "nbfeatures": 1682,
                     DOCTYPE_MOVIES:{ CSVFIELD_NAMES: ["_id", "movietitle", "releasedate", "videoreleasedate",
                                            "IMDbURL", "unknown", "Action", "Adventure", "Animation",
                                            "Childrens", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                                            "FilmNoir", "Horror", "Musical", "Mystery", "Romance", "SciFi", "Thriller",
                                            "War", "Western"] }
                     ,DOCTYPE_USERS:{CSVFIELD_NAMES: ["_id", "age", "gender", "occupation", "zip code"]}}
}
