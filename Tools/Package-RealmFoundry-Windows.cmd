@echo off
setlocal
set "RF_PROJECT=D:\CodexGames\RealmFoundry\RealmFoundry.uproject"
set "RF_ARCHIVE=D:\CodexGames\RealmFoundry\Packaged\RealmFoundry-v0.4.0-Windows"
call "D:\UE_5.8\Engine\Build\BatchFiles\RunUAT.bat" BuildCookRun -project="%RF_PROJECT%" -noP4 -platform=Win64 -clientconfig=Shipping -build -cook -allmaps -stage -pak -iostore -prereqs -archive -archivedirectory="%RF_ARCHIVE%" -additionalcookeroptions="-skipzenstore" -utf8output -unattended
exit /b %ERRORLEVEL%
