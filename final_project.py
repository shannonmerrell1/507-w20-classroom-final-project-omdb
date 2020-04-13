import requests
import json
import sqlite3
import math

conn = sqlite3.connect('movies.db')
c = conn.cursor()

api_key = "eb392c3f"
url = 'http://www.omdbapi.com/'
s = 'marvel'

params = {'s':s, 'apikey':api_key}
movie_info = requests.get(url, params=params)
# print(f"Status  code: {movie_info.status_code}")

movie_dictionary = movie_info.json()
page_length = len(movie_dictionary['Search'])

total_results = int(movie_dictionary['totalResults'])

pages = math.ceil(total_results/page_length)
print(pages)

movies_list_combined = []

for page in range(pages):
    params['page']=page + 1
    movie_page = requests.get(url, params=params).json()
    movies_list_combined += movie_page["Search"]

print(len(movies_list_combined))


# qmarks = ', '.join('?' * len(movie_dictionary))
# qry = "Insert Into Movies (%s) Values (%s)" % (qmarks, qmarks)
# c.execute(qry, movie_dictionary.keys() + movie_dictionary.values())




# google_results = requests.get('http://google.com/search?q=something')
# print(google_results.text)