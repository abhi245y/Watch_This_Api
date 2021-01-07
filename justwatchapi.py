import concurrent
import requests
import logging
from concurrent.futures.process import ProcessPoolExecutor

from constants import *


def search_items(item, movie_name, release_year, offers):
    title = item['title']
    original_release_year = item['original_release_year']
    if title == movie_name and original_release_year == release_year:
        # jw_id = item['id']
        # img_url = 'https://images.justwatch.com' + item['poster'].replace('{profile}', 's718')
        if 'offers' in item:
            for offer in item['offers']:
                if offer['monetization_type'] == streaming or offer['monetization_type'] == 'free':
                    if offer['provider_id'] == netflix and offer['presentation_type'] == 'hd':
                        netflix_url = offer['urls']['standard_web']
                        offers["Netflix"] = netflix_url
                    elif offer['provider_id'] == prime and offer['presentation_type'] == 'hd':
                        prime_url = offer['urls']['standard_web']
                        offers["Prime Videos"] = prime_url
                    elif offer['provider_id'] == sonyLiv:
                        sonyLiv_url = offer['urls']['standard_web']
                        offers["Sony Liv"] = sonyLiv_url
                    elif offer['provider_id'] == hotstar:
                        hotstar_url = offer['urls']['standard_web']
                        offers["Hotstar"] = hotstar_url
                    elif offer['provider_id'] == sunNext:
                        sunNxt_url = offer['urls']['standard_web']
                        offers["Sun Nxt"] = sunNxt_url
                    elif offer['provider_id'] == zee:
                        zee_url = offer['urls']['standard_web']
                        offers["Zee"] = zee_url
                    elif offer['provider_id'] == jioCinema:
                        jioCinema_url = offer['urls']['standard_web']
                        offers["Jio Cinema"] = jioCinema_url


def WhereToWatch(movie_name, release_year):
    offers = {}
    query = movie_name.replace(' ', '%20').replace('&', '%26')
    link = JustWatchAPI_link + query + '%22,%22content_types%22:[%22movie%22]}'
    try:
        r = requests.get(link)
        output = r.json()['items']
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_cores) as e:
            res = {e.submit(search_items, item, movie_name, release_year, offers): item for item in output}
        return offers
    except Exception as e:
        logging.exception(e)
        print("No Steaming Service Found For: " + movie_name)
