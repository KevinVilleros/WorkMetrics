@echo off
REM MetricLab - Launcher para Windows (versión limpia)
REM Este script inicia la aplicación sin abrir navegadores automáticamente

setlocal enabledelayedexpansion
color 0A

set "ROOT_DIR=%~dp0"
cd /d "%ROOT_DIR%"

echo.
echo =========================================
echo    MetricLab - Iniciador para Windows
echo =========================================
echo.

if not exist "metriclab_launcher.py" (
    echo ERROR: No se encontró metriclab_launcher.py
    echo Asegúrate de ejecutar este script desde la raíz del repositorio
    pause
    exit /b 1
)

REM Verificar que Python está disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Iniciando MetricLab...
echo.

REM Ejecutar el launcher
python metriclab_launcher.py

if errorlevel 1 (
    echo.
    echo ERROR: La aplicación no se inició correctamente
    pause
    exit /b 1
)

exit /b 0
