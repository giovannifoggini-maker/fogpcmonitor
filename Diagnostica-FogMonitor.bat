@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Diagnostica FogMonitor by FogLabs

set "PY=py -3.13"
%PY% --version >nul 2>nul
if errorlevel 1 set "PY=py -3"
%PY% --version >nul 2>nul
if errorlevel 1 goto fallback_python

echo ========================================
echo   FOGLABS - DIAGNOSTICA FOGMONITOR
echo ========================================
echo.
%PY% -c "import sys, tkinter; print('[OK] Python:', sys.version); print('[OK] Eseguibile:', sys.executable); print('[OK] Tkinter:', tkinter.TkVersion)"
if errorlevel 1 goto failed
%PY% -m py_compile FogMonitor.py
if errorlevel 1 goto failed
echo [OK] Sintassi di FogMonitor.py valida.
if exist "%LOCALAPPDATA%\FogLabs\FogMonitor\FogMonitor-error.log" (
  echo.
  echo [INFO] E' presente un log di errore precedente:
  echo "%LOCALAPPDATA%\FogLabs\FogMonitor\FogMonitor-error.log"
)
goto finish

:fallback_python
where python >nul 2>nul
if errorlevel 1 (
  echo [ERRORE] Python non trovato. Installa Python 3.10-3.13 con Tkinter.
  goto finish
)
python -c "import sys, tkinter; print('[OK] Python:', sys.version); print('[OK] Eseguibile:', sys.executable); print('[OK] Tkinter:', tkinter.TkVersion)"
if errorlevel 1 goto failed
python -m py_compile FogMonitor.py
if errorlevel 1 goto failed
echo [OK] Sintassi di FogMonitor.py valida.
goto finish

:failed
echo.
echo [ERRORE] Python, Tkinter o il codice dell'applicazione non hanno superato il controllo.
echo Conserva questo output e, se presente, invia il log diagnostico.

:finish
echo.
echo Percorso log: "%LOCALAPPDATA%\FogLabs\FogMonitor\FogMonitor-error.log"
echo Nessun dato del PC viene inviato online.
echo.
pause
