@echo off
setlocal
set "RF_PROJECT=D:\CodexGames\RealmFoundry\RealmFoundry.uproject"
set "RF_ARCHIVE=D:\CodexGames\RealmFoundry\Packaged\RealmFoundry-Tycoon-v0.3.0-Development"
call "D:\UE_5.8\Engine\Build\BatchFiles\RunUAT.bat" BuildCookRun -project="%RF_PROJECT%" -noP4 -platform=Win64 -clientconfig=Development -build -cook -allmaps -stage -pak -prereqs -archive -archivedirectory="%RF_ARCHIVE%" -utf8output -unattended
exit /b %ERRORLEVEL%
