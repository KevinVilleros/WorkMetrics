@echo off
REM ============================================================
REM MetricLab - Sistema de Detección de Personas
REM para Evaluación de Eficiencia Laboral
REM ============================================================

setlocal enabledelayedexpansion

title MetricLab - Detección de Eficiencia Laboral

echo.
echo ============================================================
echo   MetricLab v1.0
echo   Sistema de Detección de Personas y Análisis de Eficiencia
echo ============================================================
echo.

REM Verificar Python
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado en PATH
    echo.
    echo Descarga Python desde: https://www.python.org/downloads/
    echo Marca: "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [VERIFICACIÓN] Python encontrado
python --version

REM Ir a directorio del proyecto
cd /d "%~dp0"

REM Instalar dependencias si es primera ejecución
if not exist "backend\venv" (
    echo.
    echo [INSTALACIÓN] Primera ejecución detectada
    echo [INSTALACIÓN] Instalando dependencias...
    echo.
    
    REM Crear venv
    python -m venv backend\venv
    
    REM Activar y instalar
    call backend\venv\Scripts\activate.bat
    pip install --upgrade pip
    pip install -r backend\requirements-windows.txt
    
    REM Migraciones
    cd backend
    python manage.py migrate
    cd ..
)

REM Activar venv
call backend\venv\Scripts\activate.bat

echo.
echo [INICIO] Iniciando MetricLab...
echo.

REM Ejecutar launcher completo
python metriclab_complete.py

REM Si llega aquí, la aplicación terminó
echo.
pause
