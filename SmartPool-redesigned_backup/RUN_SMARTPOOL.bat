@echo off
setlocal
cd /d "%~dp0"
title SmartPool

set PY=
where py >nul 2>nul
if not errorlevel 1 set PY=py
if not defined PY (
  where python >nul 2>nul
  if not errorlevel 1 set PY=python
)
if not defined PY (
  echo.
  echo Python was not found on this computer.
  echo 1. Install Python 3.10 or newer from https://www.python.org/downloads/
  echo 2. On the first installer screen, TICK "Add python.exe to PATH".
  echo 3. Close this window and double-click RUN_SMARTPOOL.bat again.
  echo.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating a private Python environment ^(first run only^)...
  %PY% -m venv .venv
  if errorlevel 1 (
    echo Could not create the Python environment.
    pause
    exit /b 1
  )
)

echo Checking Python packages ^(first run needs internet, about a minute^)...
".venv\Scripts\python.exe" -m pip install -q -r requirements-demo.txt
if errorlevel 1 (
  echo.
  echo Package install failed. Check your internet connection and run this file again.
  pause
  exit /b 1
)

echo.
echo Starting SmartPool. Your browser will open by itself.
echo Keep this window open while you use the app. Close it or press Ctrl+C to stop.
echo.
".venv\Scripts\python.exe" run.py
echo.
pause
