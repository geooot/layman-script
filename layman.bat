@echo off
echo layman-script repl -v 0.1
echo -------------------------
:LOOP_1
set /p input="> "
call C:\Users\164543\AppData\Local\Programs\Python\Python35-32\python.exe main.py "%input%"
goto LOOP_1
