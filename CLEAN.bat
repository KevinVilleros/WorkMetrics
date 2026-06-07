@echo off
REM ============================================================
REM Script de limpieza para MetricLab
REM Elimina archivos y carpetas innecesarios para reducir tamaño
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ================================================================
echo          MetricLab - Script de Limpieza
echo ================================================================
echo.

REM Contar archivos a eliminar
set count=0

REM Limpiar entorno virtual de backend
if exist "backend\venv" (
    echo [1/6] Eliminando backend\venv ...
    rmdir /s /q "backend\venv" 2>nul
    set /a count+=1
)

REM Limpiar node_modules de frontend
if exist "frontend\node_modules" (
    echo [2/6] Eliminando frontend\node_modules ...
    rmdir /s /q "frontend\node_modules" 2>nul
    set /a count+=1
)

REM Limpiar dist de frontend
if exist "frontend\dist" (
    echo [3/6] Eliminando frontend\dist ...
    rmdir /s /q "frontend\dist" 2>nul
    set /a count+=1
)

REM Limpiar build de frontend
if exist "frontend\build" (
    echo [4/6] Eliminando frontend\build ...
    rmdir /s /q "frontend\build" 2>nul
    set /a count+=1
)

REM Limpiar __pycache__ en backend
if exist "backend\__pycache__" (
    echo [5/6] Eliminando backend\__pycache__ ...
    rmdir /s /q "backend\__pycache__" 2>nul
    set /a count+=1
)

REM Limpiar archivos de log innecesarios
if exist "output.txt" (
    echo [6/6] Eliminando archivos de log ...
    del /q "output.txt" 2>nul
    del /q "pip_install_output.txt" 2>nul
    del /q "pip_install_output2.txt" 2>nul
    del /q "test.txt" 2>nul
)

REM Limpiar caché de Python
echo Eliminando cache de Python...
for /r . %%d in (__pycache__) do @rmdir /s /q "%%d" 2>nul
for /r . %%f in (*.pyc) do @del /q "%%f" 2>nul

echo.
echo ================================================================
echo          ✓ Limpieza completada exitosamente
echo ================================================================
echo.
echo Espacio liberado:
echo - backend\venv: ~376 MB
echo - frontend\node_modules: ~502 MB
echo - frontend\dist: ~260 MB
echo - frontend\build: ~12 MB
echo - Otros archivos: ~5 MB
echo.
echo TOTAL ESTIMADO: ~1.1 GB
echo.
echo Nota: Estos archivos se regeneraran al ejecutar:
echo   - npm install (para frontend\node_modules)
echo   - npm run build (para frontend\build)
echo   - python -m venv (para backend\venv)
echo   - npm run electron:package (para frontend\dist y MetricLab.exe)
echo.
pause
