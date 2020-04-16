# covid19knowledgebase backuping
We are currently backuping our database using our local machines

## Please use **SetUpBackuping.bat**
It will create Task in the sceduler which downloads db full backup every 15 mins and put it into backup folder inside repo root 

## To setup task on on your machine

Be aware that you need:

* have powershell installed and up
* satrt your *command promt as **Admin***

Run it with providing **x-Access-token**
```SetUpBackuping.bat [x-Access-token]```