CALL mklink /d /h C:\backupknowledgebase.bat %cd%\backupknowledgebase.bat
CALL powershell -Command "(gc BackupKnowledgebase.xml) -replace '#PUT BASE DIRECTORY HERE#', '%cd%' | Out-File -encoding ASCII BackupKnowledgebase1.xml"
CALL powershell -Command "(gc BackupKnowledgebase1.xml) -replace '#PUT TOKEN HERE#', '%1' | Out-File -encoding ASCII BackupKnowledgebase1.xml"
CALL powershell -Command schtasks /create /xml "BackupKnowledgebase1.xml" /tn "\MyTasks\backupKnowledgeBaseTask" /ru "$(whoami)"
CALL DEL BackupKnowledgebase1.xml