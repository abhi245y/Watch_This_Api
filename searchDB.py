import concurrent
from constants import *
import requests as r
from datetime import datetime
from justwatchapi import WhereToWatch
from tqdm.auto import tqdm
from concurrent.futures.process import ProcessPoolExecutor

imdb_ids = []
json_data = {}


def make_json(res):
    movie_details = r.get(
        TMDB_base_link + "movie/" + str(res['id']) + "?api_key=" + TMDB_api).json()
    results = {'tmdb_id': movie_details['id'], 'imdb_id': movie_details['imdb_id'], 'title': movie_details['title'],
               'language': movie_details['original_language'], 'tmdb_rating': movie_details['vote_average'],
               'overview': movie_details['overview']}

    if movie_details['imdb_id'] is not None:
        omdb_data = r.get(OMDB_id_search_link + movie_details['imdb_id']).json()
        if omdb_data['Response'] == 'True':
            results['release_year'] = omdb_data['Year']
            results['release_date'] = omdb_data['Released']
            results['duration'] = omdb_data['Runtime']
            results['genres'] = omdb_data['Genre']
            results['imdb_rating'] = omdb_data['imdbRating']

    if movie_details['poster_path'] is not None:
        poster_link = str(TMDB_image_link + movie_details['poster_path'])
        results['poster_link'] = poster_link
    if results['imdb_id'] is not None:
        imdb_ids.append(results['imdb_id'])

    if res['release_date'] is not None and res['release_date'] != "":
        date = res['release_date'] + " 19:21:10"
        ddt = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        results['offers'] = WhereToWatch(movie_details['title'], ddt.year)
    return results


def run(req, res_len):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_cores) as executor:
        future_tmdb = list(tqdm(executor.map(make_json, req), total=res_len))
    return future_tmdb


def search_omdb(omdb_result):
    for tmdb_res in imdb_ids:
        if tmdb_res != omdb_result['imdbID']:
            omdb_data = r.get(OMDB_id_search_link + omdb_result['imdbID']).json()
            res = {'imdb_id': omdb_data['imdbID'], 'title': omdb_data['Title'], 'language': omdb_data['Language'],
                   'overview': omdb_data['Plot'], 'release_year': omdb_data['Year'],
                   'release_date': omdb_data['Released'], 'duration': omdb_data['Runtime'],
                   'genres': omdb_data['Genre'], 'poster_link': omdb_data['Poster'],
                   'imdb_rating': omdb_data['imdbRating']}
            return res


def run_omdb(omdb_results):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_cores) as executor:
        future = list(tqdm(executor.map(search_omdb, omdb_results), total=len(omdb_results)))
    return future


def searchTmdb(query):
    tmdb_req = \
        r.get(TMDB_base_link + "search/movie?api_key=" + TMDB_api + "&query=" + query).json()[
            'results']
    omdb_results = r.get(OMDB_query_search_link + query).json()['Search']
    future_result = []
    size = len(tmdb_req)
    for future in run(tmdb_req, size):
        future_result.append(future)

    for future_omdb in run_omdb(omdb_results):
        future_result.append(future_omdb)
    return future_result
