:: BatchGotAdmin
:-------------------------------------
rem SET PM=Procmon64.exe
SET PM=Procmon.exe
SET LOG=log.PML
SET CSVLOG=log.csv
SET DISKIFY=diskify.exe
SET DISKIFY_OUT=out.diskify

CD /D "%~dp0"
%PM% /terminate
START %PM% /quiet /minimized /openlog %LOG% /saveapplyfilter /saveas %CSVLOG%
%PM% /waitforidle
%PM% /terminate
:LOOP
tasklist | find /i "Procmon" >nul 2>&1
IF ERRORLEVEL 1 (
  GOTO CONTINUE
) ELSE (
  ECHO Procmon is still running
  Timeout /T 5 /Nobreak
  GOTO LOOP
)
:CONTINUE
%DISKIFY% -o %DISKIFY_OUT% %CSVLOG%

