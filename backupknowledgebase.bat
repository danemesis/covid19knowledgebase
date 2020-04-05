
CALL SET "YYYY=%DATE:~-4,4%"
CALL SET "MM=%DATE:~-7,2%" 
CALL SET "DD=%DATE:~-10,2%" 
CALL SET "HH=%TIME:~0,2%" 
CALL SET "Min=%TIME:~3,2%" 
CALL SET "Sec=%TIME:~6,2%"
CALL SET "fullstamp=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%"

CALL MKDIR backup
CALL CD backup
CALL CURL https://dan-covid19-knowledgebase.herokuapp.com/api/v1/db -o "knowledge.db"
CALL COPY knowledge.db knowledgebase_%fullstamp%.db
CALL CD ..