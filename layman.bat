@echo off
echo "_    ____ _   _ _  _ ____ _  _    ____ ____ ____ _ ___  ___"
echo "|    |__|  \_/  |\/| |__| |\ | __ [__  |    |__/ | |__]  | "
echo "|___ |  |   |   |  | |  | | \|    ___] |___ |  \ | |     | "
echo "-----------------------------------------------------------"
:LOOP_1
set /p input="> "
call C:\Users\164543\AppData\Local\Programs\Python\Python35-32\python.exe main.py "%input%"
goto LOOP_1
