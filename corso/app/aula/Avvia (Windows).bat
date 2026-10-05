@echo off
chcp 65001 >nul
title Corso patente nautica - server dell aula
cd /d "%~dp0"
if not exist "python\python.exe" goto installato
"python\python.exe" server.py
goto fine
:installato
where py >nul 2>nul && (py -3 server.py & goto fine)
where python >nul 2>nul && (python server.py & goto fine)
echo.
echo  Manca la cartella "python": scompatta di nuovo lo zip completo
echo  (tasto destro sullo zip, "Estrai tutto...").
echo.
:fine
pause
