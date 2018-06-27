RATINGS_FIELD_MOVIEID = "movieid"
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
RATINGS_FIELD_USERID = "userid"
RATINGS_FIELD_RATING = "rating"
MOVIES_FIELD_TITLE = "movietitle"
MOVIES_FIELD_RELEASEDATE = "releasedate"
DataSet = {
    DATASETID_100K: {DATASET_DESCRIPTION: "100K Data set", INDEXNAME: "hundredkds", NB_USERS: 943, NB_MOVIES: 1682, "Encoding":'ISO-8859-1',
                     DOCTYPE_MOVIES:{ CSVFIELD_NAMES: ["_id", MOVIES_FIELD_TITLE, MOVIES_FIELD_RELEASEDATE, "videoreleasedate",
                                            "IMDbURL", "unknown", "Action", "Adventure", "Animation",
                                            "Childrens", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                                            "FilmNoir", "Horror", "Musical", "Mystery", "Romance", "SciFi", "Thriller",
                                            "War", "Western"], DELIMITER: "|" }
                     , DOCTYPE_USERS:{CSVFIELD_NAMES: ["_id", USER_FIELD_AGE,  USER_FIELD_GENDER, USER_FIELD_OCCUPATION, "zip code"],  DELIMITER: "|"}
                     , DOCTYPE_RATINGS:{CSVFIELD_NAMES: [RATINGS_FIELD_USERID, RATINGS_FIELD_MOVIEID, RATINGS_FIELD_RATING, "timestamp"], DELIMITER: "\t"}

                     }
}
