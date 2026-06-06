@echo off
REM Script de ejecución para Windows (después de instalación)

setlocal enabledelayedexpansion
color 0A

set APP_DIR=%APPDATA%\MetricLab\WorkMetrics

if not exist "%APP_DIR%" (
    echo ERROR: MetricLab no está instalado
    echo Por favor, ejecuta primero: install-windows.bat
    pause
    exit /b 1
)

title MetricLab
echo.
echo Iniciando MetricLab...
echo.

REM Iniciar Backend
echo Iniciando Backend (Django) en puerto 8000...
cd /d "%APP_DIR%\backend"
call venv\Scripts\activate.bat
start "MetricLab Backend" cmd /k python manage.py runserver 8000

REM Esperar a que el backend esté listo
timeout /t 3 /nobreak

REM Iniciar Frontend
echo Iniciando Frontend (React) en puerto 3000...
cd /d "%APP_DIR%\frontend"
start "MetricLab Frontend" cmd /k npm start

echo.
echo =========================================
echo MetricLab iniciado correctamente
echo =========================================
echo.
echo Frontend:  http://localhost:3000
echo Backend:   http://localhost:8000
echo.
echo Cierra las ventanas de consola para detener
echo.
pause
