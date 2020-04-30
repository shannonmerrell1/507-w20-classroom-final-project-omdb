# 507-w20-classroom-final-project-omdb

# Project Title

Marvel Movie Database

This is a Flask program that allows users to choose a Marvel movie from a dropdown menu and learn key facts about it. It does this by creating an api from the user input and putting its id, name and other details into a database. The details of the movie are also stored in a cache file. 
Additionally, the program collects images from the google search results page and links from Duck Duck Go.  

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites


To run this you need to: 

import requests
import json
import sqlite3
import math
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import re

Write these lines at the top of your code. 

```
Give examples
```

### Installing

To get a development environment running, set up a gitignore file with secrets.py
Store your API key in secrets.py. Obtain an OMDB API key here: 
To access this, 
Store your API key in a variable

Here the API Key is located . 



Set up your database by 
Connect to it with 

example

Set up an instance of the Flask class with
app = Flask(__name__)


example



## Additional


```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc