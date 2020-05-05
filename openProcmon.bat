:: BatchGotAdmin
:-------------------------------------
rem SET PM=Procmon64.exe
SET PM=Procmon.exe
SET LOG=log.pml

CD /D "%~dp0"
START %PM% /quiet /minimized /backingfile %LOG%
exit 0
