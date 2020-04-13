import requests
import json
import sqlite3

conn = sqlite3.connect('movies.db')
c = conn.cursor()

api_key = "eb392c3f"
url = 'http://www.omdbapi.com/'

title = input("Pick a movie:")

url = url + '?T=' + title + '&apikey=' + api_key

print(url)

movie_info = requests.get(url)
# print(f"Status  code: {movie_info.status_code}")

movie_dictionary = movie_info.json()

qmarks = ', '.join('?' * len(movie_dictionary))
qry = "Insert Into Movies (%s) Values (%s)" % (qmarks, qmarks)
c.execute(qry, movie_dictionary.keys() + movie_dictionary.values())

print(movie_dictionary.keys())


# google_results = requests.get('http://google.com/search?q=something')
# print(google_results.text)