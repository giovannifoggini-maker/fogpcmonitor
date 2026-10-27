@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Build FogMonitor by FogLabs

set "PY=py -3.13"
%PY% --version >nul 2>nul
if errorlevel 1 set "PY=py -3"
%PY% --version >nul 2>nul
if errorlevel 1 (
  echo [ERRORE] Python non trovato. Installa Python 3.10-3.13 e includi il Python Launcher.
  pause
  exit /b 1
)

echo.
echo  FogMonitor by FogLabs - build Windows
 echo [1/4] Controllo sintassi e test helper...
%PY% -m py_compile FogMonitor.py
if errorlevel 1 goto failed
%PY% -m unittest discover -s tests -v
if errorlevel 1 goto failed

echo [2/4] Installazione degli strumenti di build...
%PY% -m pip install --upgrade -r requirements-build.txt
if errorlevel 1 goto failed

echo [3/4] Creazione di FogMonitor.exe...
%PY% -m PyInstaller --noconfirm --clean --onefile --windowed --name FogMonitor --icon "assets\fogmonitor.ico" --version-file "version_info.txt" --add-data "assets;assets" "FogMonitor.py"
if errorlevel 1 goto failed

if not exist release mkdir release
copy /y "README-PORTABLE.txt" "dist\README-FogMonitor.txt" >nul
if exist "release\FogMonitor-by-FogLabs-Windows.zip" del /q "release\FogMonitor-by-FogLabs-Windows.zip"
echo [4/4] Creazione dello ZIP portabile...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path 'dist\FogMonitor.exe','dist\README-FogMonitor.txt','LICENSE.txt' -DestinationPath 'release\FogMonitor-by-FogLabs-Windows.zip' -Force"
if errorlevel 1 goto failed

echo.
echo BUILD COMPLETATA
 echo EXE: dist\FogMonitor.exe
 echo ZIP: release\FogMonitor-by-FogLabs-Windows.zip
 echo.
pause
exit /b 0

:failed
echo.
echo [ERRORE] Build non completata. Controlla il messaggio precedente.
echo Suggerimento: verifica che pip abbia accesso a Internet e riprova.
pause
exit /b 1
