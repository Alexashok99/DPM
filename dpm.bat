@echo off
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH.
    pause
    exit /b
)

python "C:\MyTools\main.py" %*
pause
