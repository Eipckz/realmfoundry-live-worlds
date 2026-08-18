@echo off
setlocal
for %%I in ("%~dp0..") do set "RF_ROOT=%%~fI"
if not defined UE_ROOT set "UE_ROOT=D:\UE_5.8"
set "RF_PROJECT=%RF_ROOT%\RealmFoundry.uproject"
set "RF_ARCHIVE=%RF_ROOT%\Packaged\RealmFoundry-v0.4.0-Windows"
call "%UE_ROOT%\Engine\Build\BatchFiles\RunUAT.bat" BuildCookRun -project="%RF_PROJECT%" -noP4 -platform=Win64 -clientconfig=Shipping -build -cook -allmaps -stage -pak -iostore -prereqs -archive -archivedirectory="%RF_ARCHIVE%" -additionalcookeroptions="-skipzenstore" -utf8output -unattended
exit /b %ERRORLEVEL%
