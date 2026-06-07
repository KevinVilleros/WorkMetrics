@echo off
REM Script de instalación para Windows
REM Requiere: Python 3.10+, Node.js 16+, PostgreSQL 13+

setlocal enabledelayedexpansion
color 0A

echo.
echo ========================================
echo MetricLab - Sistema de Monitoreo Laboral
echo Instalador para Windows
echo ========================================
echo.

REM Verificar Python
echo [1/5] Verificando Python 3...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3 no está instalado o no está en PATH
    echo Descarga desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Verificar Node.js
echo [2/5] Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js no está instalado o no está en PATH
    echo Descarga desde: https://nodejs.org/
    pause
    exit /b 1
)

REM Crear directorio de instalación
set APP_DIR=%APPDATA%\MetricLab
if not exist "%APP_DIR%" mkdir "%APP_DIR%"
cd /d "%APP_DIR%"

echo [3/5] Descargando aplicación...
if exist "WorkMetrics" (
    cd WorkMetrics
    git pull
) else (
    git clone https://github.com/KevinVilleros/WorkMetrics.git
    cd WorkMetrics
)

REM Backend setup
echo [4/5] Configurando Backend (Python)...
cd backend

if not exist "venv" (
    python -m venv venv
)

call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Crear .env si no existe
if not exist ".env" (
    copy .env.example .env
    echo.
    echo Archivo .env creado. Por favor, edita %APP_DIR%\WorkMetrics\backend\.env
    pause
)

REM Ejecutar migraciones
python manage.py migrate

cd ..

REM Frontend setup
echo [5/5] Configurando Frontend (React)...
cd frontend
call npm install
cd ..

REM Crear scripts batch
echo Creando accesos directos...

REM Script para iniciar
(
    echo @echo off
    echo title MetricLab
    echo set APP_DIR=%APP_DIR%\WorkMetrics
    echo echo.
    echo echo Iniciando MetricLab...
    echo echo.
    echo cd /d "!APP_DIR!\backend"
    echo call venv\Scripts\activate.bat
    echo echo Iniciando Backend en puerto 8000...
    echo start cmd /k python manage.py runserver 8000
    echo timeout /t 3
    echo cd /d "!APP_DIR!\frontend"
    echo echo Iniciando Frontend en puerto 3000...
    echo start cmd /k npm start
    echo echo.
    echo echo Frontend: http://localhost:3000
    echo echo Backend: http://localhost:8000
    echo pause
) > "%APP_DIR%\start-metriclab.bat"

REM Script para detener
(
    echo @echo off
    echo echo Deteniendo MetricLab...
    echo taskkill /F /IM python.exe >nul 2>&1
    echo taskkill /F /IM node.exe >nul 2>&1
    echo echo Detenido
    echo pause
) > "%APP_DIR%\stop-metriclab.bat"

REM Crear acceso directo en escritorio
powershell -NoProfile -Command ^
    "$WshShell = New-Object -ComObject WScript.Shell; " ^
    "$Shortcut = $WshShell.CreateShortcut('$env:Public\Desktop\MetricLab.lnk'); " ^
    "$Shortcut.TargetPath = '%APP_DIR%\start-metriclab.bat'; " ^
    "$Shortcut.WorkingDirectory = '%APP_DIR%'; " ^
    "$Shortcut.IconLocation = 'cmd.exe, 0'; " ^
    "$Shortcut.Save()"

REM Crear acceso directo en Inicio
powershell -NoProfile -Command ^
    "$WshShell = New-Object -ComObject WScript.Shell; " ^
    "$StartMenuPath = [Environment]::GetFolderPath('StartMenu'); " ^
    "$Shortcut = $WshShell.CreateShortcut(\"$StartMenuPath\Programs\MetricLab.lnk\"); " ^
    "$Shortcut.TargetPath = '%APP_DIR%\start-metriclab.bat'; " ^
    "$Shortcut.WorkingDirectory = '%APP_DIR%'; " ^
    "$Shortcut.IconLocation = 'cmd.exe, 0'; " ^
    "$Shortcut.Save()"

echo.
echo ========================================
echo Instalación completada
echo ========================================
echo.
echo Para iniciar la aplicación:
echo   Busca "MetricLab" en el menú Inicio
echo   O ejecuta: %APP_DIR%\start-metriclab.bat
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo.
pause
