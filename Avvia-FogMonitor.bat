@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title FogMonitor by FogLabs

rem Preferisce il lancio grafico senza console. In caso di problemi usa
rem il percorso console, che conserva i messaggi diagnostici.
where py >nul 2>nul
if not errorlevel 1 goto via_launcher
where pythonw.exe >nul 2>nul
if not errorlevel 1 goto via_pythonw
where python.exe >nul 2>nul
if not errorlevel 1 goto via_python

echo.
echo [FogMonitor] Python non e' stato trovato.
echo Serve Python 3.10-3.13 con Tkinter incluso.
echo.
pause
exit /b 1

:via_launcher
py -3.13 --version >nul 2>nul
if not errorlevel 1 (
    where pyw >nul 2>nul
    if not errorlevel 1 (
        start "" pyw -3.13 FogMonitor.py
        exit /b 0
    )
    py -3.13 FogMonitor.py
    set "APP_EXIT=%ERRORLEVEL%"
    goto after_run
)
py -3 --version >nul 2>nul
if not errorlevel 1 (
    where pyw >nul 2>nul
    if not errorlevel 1 (
        start "" pyw -3 FogMonitor.py
        exit /b 0
    )
    py -3 FogMonitor.py
    set "APP_EXIT=%ERRORLEVEL%"
    goto after_run
)
echo [FogMonitor] Il Python Launcher esiste, ma non trovo un runtime Python utilizzabile.
goto fallback_python

:via_pythonw
start "" pythonw.exe FogMonitor.py
exit /b 0

:via_python
python.exe FogMonitor.py
set "APP_EXIT=%ERRORLEVEL%"
goto after_run

:fallback_python
where python.exe >nul 2>nul
if not errorlevel 1 goto via_python
echo Installa Python 3.10-3.13 includendo Tcl/Tk, quindi riprova.
echo.
pause
exit /b 1

:after_run
if not "%APP_EXIT%"=="0" (
    echo.
    echo [FogMonitor] Avvio terminato con codice %APP_EXIT%.
    if exist "FogMonitor-error.log" (
        echo --- Ultimo errore registrato ---
        type "FogMonitor-error.log"
        echo --- Fine errore ---
    )
    echo.
    pause
)
exit /b %APP_EXIT%
