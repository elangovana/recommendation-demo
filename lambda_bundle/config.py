
DATASETID_100K = "100KDS"
DOCTYPE_MOVIES ="movies"
DOCTYPE_USERS="users"
DOCTYPE_RATINGS="ratings"
CSVFIELD_NAMES="fieldnames"
NB_USERS="nbusers"
NB_MOVIES="nbMovies"
DELIMITER ="Delimiter"
INDEXNAME="index_name"

USER_FIELD_AGE = "age"
USER_FIELD_GENDER = "gender"
USER_FIELD_OCCUPATION = "occupation"

DATASET_DESCRIPTION = "name"
DataSet = {
    DATASETID_100K: {DATASET_DESCRIPTION: "100K Data set", INDEXNAME: "hundredkds", NB_USERS: 943, NB_MOVIES: 1682, DELIMITER: "|",
                     DOCTYPE_MOVIES:{ CSVFIELD_NAMES: ["_id", "movietitle", "releasedate", "videoreleasedate",
                                            "IMDbURL", "unknown", "Action", "Adventure", "Animation",
                                            "Childrens", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                                            "FilmNoir", "Horror", "Musical", "Mystery", "Romance", "SciFi", "Thriller",
                                            "War", "Western"] }
                     , DOCTYPE_USERS:{CSVFIELD_NAMES: ["_id", USER_FIELD_AGE,  USER_FIELD_GENDER, USER_FIELD_OCCUPATION, "zip code"]}
                     , DOCTYPE_RATINGS:{CSVFIELD_NAMES: ["userid" , "movieid" , "rating", "timestamp"]}

                     }
}
