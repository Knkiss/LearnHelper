@echo off
title Building ExamHelper

:: Set output name
set VERSION=0.4
set OUTPUT_NAME=ExamHelperClient_%VERSION%

echo [1] Cleaning previous build files...
rd /s /q build
rd /s /q dist
del /q %OUTPUT_NAME%.spec

echo [2] Building %OUTPUT_NAME%.exe with PyInstaller...
pyinstaller -F --name %OUTPUT_NAME% -i icon.ico main.py

echo [3] Moving EXE to current directory...
move /Y dist\%OUTPUT_NAME%.exe . >nul

echo [4] Cleaning temporary files...
rd /s /q build
rd /s /q dist
del /q %OUTPUT_NAME%.spec

:: Optional: clean pycache and temp files
for /d /r %%i in (__pycache__) do rd /s /q "%%i"
del /s /q *.log >nul 2>nul
del /s /q *.pyc >nul 2>nul

echo.
echo Build complete. Only %OUTPUT_NAME%.exe has been preserved.
echo.

pause
