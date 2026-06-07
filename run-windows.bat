@echo off
REM Script de ejecución para Windows desde la raíz del repositorio local

setlocal enabledelayedexpansion
color 0A

set "ROOT_DIR=%~dp0"
cd /d "%ROOT_DIR%"

echo =========================================
echo Iniciando MetricLab desde:
echo %ROOT_DIR%
echo =========================================

if not exist "%ROOT_DIR%backend\" (
    echo ERROR: No se encontró la carpeta backend.
    echo Asegúrate de ejecutar este script desde la raíz del repositorio.
    pause
    exit /b 1
)
if not exist "%ROOT_DIR%frontend\" (
    echo ERROR: No se encontró la carpeta frontend.
    echo Asegúrate de ejecutar este script desde la raíz del repositorio.
    pause
    exit /b 1
)

REM Preparar backend
cd /d "%ROOT_DIR%backend"
if not exist "venv\Scripts\activate.bat" (
    echo Creando entorno virtual en backend\venv...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual. Comprueba que Python 3.10+ esté instalado.
        pause
        exit /b 1
    )
)

call venv\Scripts\activate.bat

echo Actualizando pip, setuptools y wheel a la última versión...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo ERROR: Fallo al actualizar pip, setuptools o wheel.
    pause
    exit /b 1
)

if not exist ".env" (
    echo Generando archivo .env local para SQLite...
    >".env" (
        echo DEBUG=True
        echo SECRET_KEY=django-insecure-replace-me
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
        echo CORS_ALLOW_ALL_ORIGINS=False
    )
)

echo Instalando dependencias del backend para Windows...
python -m pip install --prefer-binary --upgrade --force-reinstall -r requirements-windows.txt
if errorlevel 1 (
    echo ERROR: Fallo al instalar dependencias del backend.
    pause
    exit /b 1
)

echo Ejecutando migraciones de Django...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Fallo al ejecutar las migraciones.
    pause
    exit /b 1
)

start "MetricLab Backend" cmd /k "cd /d \"%ROOT_DIR%backend\" && call venv\Scripts\activate.bat && python manage.py runserver 8000"

REM Preparar frontend
cd /d "%ROOT_DIR%frontend"
if not exist "node_modules\" (
    echo Instalando dependencias del frontend...
    npm install
    if errorlevel 1 (
        echo ERROR: Fallo al instalar dependencias del frontend.
        pause
        exit /b 1
    )
)

echo Iniciando Frontend (React) en puerto 3000...
start "MetricLab Frontend" cmd /k "cd /d \"%ROOT_DIR%frontend\" && npm start"

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
