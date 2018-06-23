DATASETID_100K = "hundredkds"
DOCTYPE_MOVIES ="movies"
DOCTYPE_USERS="users"
DOCTYPE_RATINGS="ratings"
CSVFIELD_NAMES="fieldnames"
NB_USERS="nbusers"
NB_MOVIES="nbMovies"
DELIMITER ="Delimiter"

DataSet = {
    DATASETID_100K: {"name": "100K Data set", NB_USERS: 943, NB_MOVIES: 1682,DELIMITER:"|",
                     DOCTYPE_MOVIES:{ CSVFIELD_NAMES: ["_id", "movietitle", "releasedate", "videoreleasedate",
                                            "IMDbURL", "unknown", "Action", "Adventure", "Animation",
                                            "Childrens", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                                            "FilmNoir", "Horror", "Musical", "Mystery", "Romance", "SciFi", "Thriller",
                                            "War", "Western"] }
                     ,DOCTYPE_USERS:{CSVFIELD_NAMES: ["_id", "age", "gender", "occupation", "zip code"]}
                     , DOCTYPE_RATINGS:{CSVFIELD_NAMES: ["userid" , "movieid" , "rating", "timestamp"]}

                     }
}
