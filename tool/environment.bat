:: Disable debug print
@echo off

:: Go one folder up to repository root
cd %~dp0\..

:: Set up virtual environment and install requirements there if needed
if not exist "%cd%\Scripts\activate" (
	virtualenv . --system-site-packages
	call Scripts\activate
	pip install -r requirements.txt
)

:: Start command prompt, activate virtual environment and clear screen
cmd /K "Scripts\activate & cls"
