CALL heroku container:login
CALL heroku container:push web --app=covid19knowledgebase
CALL heroku container:release web --app=covid19knowledgebase
CALL heroku open --app=covid19knowledgebase
CALL curl https://covid19knowledgebase.herokuapp.com/api/v1/ping