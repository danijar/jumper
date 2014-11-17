:: Disable debug print
@echo off

:: Go one folder up to repository root
cd %~dp0\..

:: Activate virtual environment and clear screen
call Scripts\activate
cls

:: Run entry script with Python
python src\main.py

:: On crash, hold console open to read error messages
if errorlevel 1 pause
