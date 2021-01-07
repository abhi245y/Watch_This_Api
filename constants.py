import multiprocessing

TMDB_base_link = 'https://api.themoviedb.org/3/'
TMDB_api = '7d8ad71f7e277923665d1197cb77e46b'
TMDB_image_link = 'https://image.tmdb.org/t/p/original'
OMDB_id_search_link = 'http://www.omdbapi.com/?apikey=9a7a1eb3&i='
OMDB_query_search_link = 'http://www.omdbapi.com/?apikey=9a7a1eb3&s='
netflix = 8
prime = 119
sonyLiv = 237
hotstar = 122
sunNext = 309
jioCinema = 220
zee = 232
JustWatchAPI_link = 'https://apis.justwatch.com/content/titles/en_IN/popular?body={%22page_size%22:5,%22page%22:1,%22query%22:%22'
streaming = 'flatrate'
num_cores = multiprocessing.cpu_count()
