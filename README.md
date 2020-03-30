# covid19knowledgebase
It is the knowledgebase for COVID-19 related questions with links. **Not prodiction ready**
We definitely need Python guru here who can put code & python architecture of the application on the next level.

## Main dependencies
- flask (for handling incoming requests and hot reloading)
- <a href='https://github.com/seatgeek/fuzzywuzzy'>fuzzywuzzy</a> (for finding answers in **knowledgebase** on incoming questions). <a href='https://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/'>More about it 1</a>, <a href='https://www.datacamp.com/community/tutorials/fuzzy-string-python'>More 2</a>

## Run
#### Prerequirements
- python version 3.8.1
- pip version 20.0.2 
- flask version 1.1.1

#### Once
##### **Windows, x64**
- `set FLASK_APP=flaskr`
- `set FLASK_ENV=development`

#### Start
- `flask run`
