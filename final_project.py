import requests
import json
import sqlite3
import math

conn = sqlite3.connect('movies.db')
c = conn.cursor()

api_key = "eb392c3f"
base_url = 'http://www.omdbapi.com/'
# s = 'marvel'
my_cache = {}

CACHE_FILENAME = "movies_cache.json"

def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME, "w")
    fw.write(dumped_json_cache)
    fw.close()


def construct_url(genre_marvel):
    url = base_url + '?s=' + genre_marvel + '&apikey=' + api_key
    print (url)
    return url


def construct_id_url(imdbid):
    url = base_url + '?i=' + imdbid + '&apikey=' + api_key 
    return url

def make_search_api_request(url, my_cache, params={}):

    # cache_key = construct_url(genre_marvel)
        response = requests.get(url, params=params).json()
        return response


 
def download_repeat_marvel_movies():

    
    url = construct_url('marvel')
    movie_dictionary = make_search_api_request(url, my_cache)
    page_length = len(movie_dictionary['Search'])
    total_results = int(movie_dictionary['totalResults'])
    pages = math.ceil(total_results/page_length)
    print(pages)

    movies_list_combined = []
    movies_found = set()
    for page in range(pages):
        params = {}
        params['page']=page + 1
        movie_page = make_search_api_request(url, my_cache, params=params)
        for movie in movie_page['Search']:
            imdbID = movie['imdbID']
            if imdbID not in movies_found: 
                movies_list_combined.append(movie)
                movies_found.add(imdbID)

    # print(len(movies_list_combined))
    return movies_list_combined


def key_values_to_list(dictionary, my_keys):
    results_imdb = []
    for key in my_keys: 
        results_imdb.append(dictionary[key])
    return results_imdb


drop_movies = '''
    DROP TABLE IF EXISTS "Movies";
'''

create_movies = '''
    CREATE TABLE IF NOT EXISTS "Movies" (
        "IMDBID"       TEXT PRIMARY KEY,
        "Title"        TEXT NOT NULL 
    )
'''

insert_id_title = '''
    INSERT INTO Movies
    VALUES (?, ?)
    '''


if __name__ == "__main__":
    # user_input = input("What movie would you like to query?")
 
    cache_dict = open_cache()

    movie_list_combined = download_repeat_marvel_movies()



#put the characteristics of the movie length combined into sql 
#get the id from sql with the user input title, then translate id to an api search
#then with the api search put all of the characteristics into json, the local cache
#then give the characteristics back to the user. 

    c.execute(drop_movies) 
    c.execute(create_movies)   
    conn.commit()


    for movie in movie_list_combined:
        list_for_sql = key_values_to_list(movie, ['imdbID', 'Title'])
        print(list_for_sql)
        c.execute(insert_id_title, list_for_sql)
   
    conn.commit()
   

    for movie in movie_list_combined:
        # print(movie) 
        id = movie['imdbID']
        url = construct_id_url(id)

        if url in my_cache: 
            long_movie_dict = my_cache[url] 
        else: 
            long_movie_dict = requests.get(url).json()
            cache_dict[url] = long_movie_dict
    print(long_movie_dict.keys())
    
    save_cache(cache_dict)

    
    



# # print(movies_list_combined[:3])
# movie_count = c.execute("Select count(*) from movies")
# if movie_count < 1:
#     params = {'s':s, 'apikey':api_key}
#     make_search_api_request(url, params=params)
    

# for movie in movies_list_combined:
#     print(movie['Title'])
#     print("="*7,movie.keys())
#     query = '''
#         INSERT INTO Movies (Title, Year, ImdbId)
#         VALUES (?,?,?,?,?,?,?,?)
#         '''
#     values = [movie.get('Title'), int(movie.get('Year')), movie.get('Rated'), int(movie.get('Released')), movie.get('Runtime'), movie.get('Genre'), movie.get('Director'), movie.get('Actors')]
    
#     c.execute(query,values)

# conn.commit()



# google_results = requests.get('http://google.com/search?q=something')
# print(google_results.text)
    





    
    
