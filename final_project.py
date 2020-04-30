import requests
import json
import sqlite3
import math
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import re
import secrets
api_omdb = secrets.omdb_api_key
api_nyt = secrets.nyt_api_key

db_name = 'movies.db'
conn = sqlite3.connect(db_name)
c = conn.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') # just the static HTML


@app.route('/handle_form', methods=['GET','POST'])
def handle_the_form():

    
    movie = request.form["movie"]
    
    query_sql = 'SELECT * FROM MOVIES WHERE TITLE= "{}"'.format(movie)
    connection = sqlite3.connect(db_name)
    cur = connection.cursor() 
    
    # print(query_sql)

    results = cur.execute(query_sql)   
    result = cur.fetchone()
    imdbID = result[0]

    return add_movie_details(imdbID)
    

@app.route('/details/<imdbid>', methods=['GET'])
def add_movie_details(imdbid):

    details = get_movie_dictionary_details(imdbid)
    movie_name= details['Title']
    release_year= details['Year']
    director= details['Director']
    actors= details['Actors']
    gross = details.get('BoxOffice', 'Unknown')

    end_point_google='http://google.com/search' 
    google_results = requests.get(end_point_google, params= {'q':movie_name})
    soup = BeautifulSoup(google_results.text, 'html.parser')
    images_news_list = []
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        images_news_list.append(link.get('href'))

    images = images_news_list[1]


    url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
    print(api_nyt)
    resp_dict = requests.get(url, params={"q":movie_name, 'fq': 'news_desk:Movies', "api-key": api_nyt}).json()
    # print(resp_dict)
    


    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    pictures = []
    for item in (resp_dict['response']['docs']):
        multimedia = item.get('multimedia')
        if multimedia:
            pic_url= 'https://static01.nyt.com/'+multimedia[0]['url']
            pictures.append(pic_url)
    print(pictures)


    # for image_url in images:
    #      cursor.execute(insert_images_url, (imdbid, image_url))
    # conn.commit()

    
    return render_template('details.html', 
                    movie_name= movie_name,
                    release_year= release_year,
                    director= director, 
                    actors= actors, 
                    gross= gross, 
                    images= images,
                    len = len(pictures),
                    pictures= pictures)


    




base_url = 'http://www.omdbapi.com/'
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


def construct_url(search_word):
    url = base_url + '?s=' + search_word + '&apikey=' + api_omdb
    # print (url)
    return url

def construct_duck_url(search_word):
    url = duck_url + '?s=' + search_word


def construct_id_url(imdbid):
    url = base_url + '?i=' + imdbid + '&apikey=' + api_omdb
    return url

def make_search_api_request(url, my_cache, params={}):
        response = requests.get(url, params=params).json()
        return response


 

def download_repeat_marvel_movies():
    movies_found = set()
    movies_list_combined = []
    movie_titles = ["Iron Man", "Thor", "The Incredible Hulk", "Avengers", "Captain America", "Guardians of the Galaxy", "Dr. Strange", "Antman", "Civil War",
    "Spider Man", "Incredible Hulk"]
    for movie in movie_titles:
        url = construct_url(movie)
        movie_dictionary = make_search_api_request(url, my_cache)
        page_length = len(movie_dictionary['Search'])
        total_results = int(movie_dictionary['totalResults'])
        pages = math.ceil(total_results/page_length)
        # print(pages)

        
        for page in range(pages):
            params = {}
            params['page']=page + 1
            movie_page = make_search_api_request(url, my_cache, params=params)
            for movie in movie_page['Search']:
                imdbID = movie['imdbID']
                if imdbID not in movies_found:
                    movies_list_combined.append(movie)
                    movies_found.add(imdbID)

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

drop_images = '''
    DROP TABLE IF EXISTS "Images";
'''

create_images = '''
    CREATE TABLE IF NOT EXISTS "Images" (
        "ROW_ID" AUTO INCREMENT PRIMARY KEY,
        "IMDBID"  TEXT NOT NULL, 
        "IMAGE_URL"  TEXT NOT NULL
    )
'''

insert_images_url = '''
    INSERT INTO Images 
    VALUES (NULL, ?, ?)
'''
 

def get_movie_dictionary_details(id):
    url = construct_id_url(id)

    if url in my_cache: 
        long_movie_dict = my_cache[url] 
    else: 
        long_movie_dict = requests.get(url).json()
        cache_dict[url] = long_movie_dict
    
    return long_movie_dict



if __name__ == "__main__":
    
    cache_dict = open_cache()

    # movie_list_combined = download_repeat_marvel_movies()
    # c.execute(drop_movies) 
    # c.execute(create_movies)   
    # conn.commit()
    # for movie in movie_list_combined:
    #     list_for_sql = key_values_to_list(movie, ['imdbID', 'Title'])
    #     c.execute(insert_id_title, list_for_sql)
    # conn.commit()

    c.execute(drop_images)
    c.execute(create_images)
    conn.commit()
    conn.close()


    save_cache(cache_dict)

    app.run(debug=True)
    



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
    





    
    
