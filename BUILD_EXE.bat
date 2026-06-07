@echo off
REM ============================================================
REM Script para compilar MetricLab.exe (Electron + Windows)
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ================================================================
echo          MetricLab - Generador de Ejecutable (Electron)
echo ================================================================
echo.

REM Verificar que npm está disponible
where npm >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm no encontrado en PATH
    echo.
    echo Instala Node.js desde: https://nodejs.org
    echo.
    pause
    exit /b 1
)

echo [1/5] Verificando dependencias...
cd /d "%~dp0frontend"

if not exist "node_modules" (
    echo [2/5] Instalando dependencias (npm install)...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Fallo al instalar dependencias
        pause
        exit /b 1
    )
) else (
    echo [2/5] node_modules ya existe (skipping npm install)
)

echo [3/5] Limpiando compilaciones anteriores...
if exist "dist" rmdir /s /q "dist" 2>nul
if exist "build" rmdir /s /q "build" 2>nul

echo [4/5] Compilando React (npm run build)...
call npm run build
if errorlevel 1 (
    echo [ERROR] Fallo al compilar React
    pause
    exit /b 1
)

echo [5/5] Empaquetando Electron (npm run electron:package)...
call npm run electron:package
if errorlevel 1 (
    echo [ERROR] Fallo al empaquetar Electron
    pause
    exit /b 1
)

echo.
echo ================================================================
echo          ✓ Compilación exitosa
echo ================================================================
echo.
echo Ejecutable generado en:
echo.
echo   %CD%\dist\MetricLab-win32-x64\MetricLab.exe
echo.
echo Prueba el ejecutable:
echo   %CD%\dist\MetricLab-win32-x64\MetricLab.exe
echo.
echo ================================================================
echo.
pause
