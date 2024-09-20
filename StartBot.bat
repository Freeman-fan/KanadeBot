@echo off

call activate QQbot-py3d9
set NOW=%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%-%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
if not exist .\log mkdir .\log
:: python bot.py > .\log\%NOW%-log.log 2>&1
start /B "" "python" "bot.py" > .\log\%NOW%-log.log 2>&1
echo bot was started up, close this window to stop it.

call tail -f .\log\%NOW%-log.log

pause