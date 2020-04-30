# 507-w20-classroom-final-project-omdb

# Project Title

Marvel Movie Database

This is a Flask program that allows users to choose a Marvel movie from a dropdown menu and learn key facts about it. It does this by creating an api from the user input and putting its id, name and other details into a database. The details of the movie are also stored in a cache file. 
Additionally, the program collects images from the google search results page and image urls from the New York Times. 



### Prerequisites


To run this you need to: 

import requests
import json
import sqlite3
import math
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import re


```

### Installing

To get a development environment running, set up a gitignore file with secrets.py

Get an OMDB API: http://www.omdbapi.com/apikey.aspx
Get an NYT API: https://developer.nytimes.com/


Set up a Flask class with
app = Flask(__name__)



## Additional

Use the program by selecting a Marvel movie from the drop down menu.  


