@echo off
REM ============================================================
REM Script para compilar MetricLab como ejecutable standalone
REM Genera: MetricLab.exe (incluye TODO)
REM ============================================================

setlocal enabledelayedexpansion

title MetricLab - Compilador Ejecutable Standalone

echo.
echo ============================================================
echo   MetricLab - Generador de Ejecutable Standalone
echo ============================================================
echo.

REM Verificar Python
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado
    echo.
    echo Descarga: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Verificar npm para compilar React
where npm >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm no encontrado
    echo.
    echo Descarga: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

cd /d "%~dp0"

echo [1/6] Verificando dependencias...
python --version
npm --version

REM Compilar React
echo.
echo [2/6] Compilando React...
cd frontend
if not exist "build" (
    echo [COMPILANDO] npm run build...
    call npm run build
    if errorlevel 1 (
        echo [ERROR] Fallo compilar React
        cd ..
        pause
        exit /b 1
    )
)
cd ..

echo ✓ Build React completado

REM Instalar PyInstaller
echo.
echo [3/6] Verificando PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [INSTALANDO] PyInstaller...
    python -m pip install pyinstaller
)

echo ✓ PyInstaller listo

REM Preparar requirements para PyInstaller
echo.
echo [4/6] Preparando dependencias...

set requirements_temp=requirements_pyinstaller.txt
(
    echo Django^>=4.2,^<5.0
    echo djangorestframework^>=3.14.0
    echo django-cors-headers^>=4.0.0
    echo mediapipe^>=0.10.0
    echo opencv-python^>=4.8.0
    echo numpy^>=1.24.0
    echo pillow^>=10.0.0
    echo requests^>=2.31.0
    echo gunicorn^>=21.0.0
) > %requirements_temp%

python -m pip install -r %requirements_temp% -q

echo ✓ Dependencias instaladas

REM Compilar con PyInstaller
echo.
echo [5/6] Compilando ejecutable...
echo [COMPILACIÓN] Esto puede tomar 5-10 minutos...
echo.

python -m PyInstaller --onefile ^
    --windowed ^
    --name MetricLab ^
    --icon="frontend/public/favicon.ico" ^
    --add-data "frontend/build;frontend/build" ^
    --add-data "backend;backend" ^
    --add-data "docs;docs" ^
    --hidden-import=django ^
    --hidden-import=django.conf ^
    --hidden-import=rest_framework ^
    --hidden-import=corsheaders ^
    --hidden-import=mediapipe ^
    --hidden-import=cv2 ^
    --hidden-import=numpy ^
    metriclab_complete.py

if errorlevel 1 (
    echo [ERROR] Fallo en compilación PyInstaller
    pause
    exit /b 1
)

echo.
echo [6/6] Validación y limpieza...

REM Verificar que se creó el .exe
if exist "dist\MetricLab.exe" (
    echo ✓ Ejecutable creado exitosamente
    
    REM Calcular tamaño
    for /f "tokens=5" %%a in ('dir dist\MetricLab.exe ^| find "MetricLab.exe"') do (
        echo   Tamaño: %%a bytes
    )
) else (
    echo [ERROR] No se creó MetricLab.exe
    pause
    exit /b 1
)

REM Limpiar temporales
del /q %requirements_temp% 2>nul
rmdir /s /q build 2>nul
rmdir /s /q "__pycache__" 2>nul

echo.
echo ============================================================
echo ✓ COMPILACIÓN COMPLETADA EXITOSAMENTE
echo ============================================================
echo.
echo Ubicación: dist\MetricLab.exe
echo.
echo Próximos pasos:
echo 1. Prueba: dist\MetricLab.exe
echo 2. Distribuye: Carpeta dist\ a usuarios
echo.

pause
