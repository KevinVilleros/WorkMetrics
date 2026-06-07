#!/usr/bin/env python3
"""
MetricLab Windows Launcher
Ejecutable que inicia la aplicación de forma limpia en Windows
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
from typing import Optional, Tuple
import threading
import socket

# Detectar el directorio raíz del proyecto
PROJECT_ROOT = Path(__file__).parent.absolute()
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
VENV_DIR = BACKEND_DIR / "venv"
ENV_FILE = BACKEND_DIR / ".env"


def log(message: str, level: str = "INFO"):
    """Registrar mensajes con timestamp"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    prefix = f"[{timestamp}] [{level}]"
    print(f"{prefix} {message}")


def check_port_available(port: int) -> bool:
    """Verificar si un puerto está disponible"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0


def create_venv() -> bool:
    """Crear entorno virtual"""
    if VENV_DIR.exists():
        log(f"Entorno virtual ya existe en {VENV_DIR}")
        return True
    
    log("Creando entorno virtual...")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
        log("Entorno virtual creado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        log(f"Error creando entorno virtual: {e}", "ERROR")
        return False


def get_python_exe() -> Path:
    """Obtener la ruta del ejecutable de Python en el venv"""
    if sys.platform == "win32":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def upgrade_pip() -> bool:
    """Actualizar pip, setuptools y wheel"""
    python_exe = get_python_exe()
    log("Actualizando pip, setuptools y wheel...")
    try:
        subprocess.run(
            [str(python_exe), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"],
            check=True,
            capture_output=True
        )
        log("pip actualizado")
        return True
    except subprocess.CalledProcessError as e:
        log(f"Error actualizando pip: {e}", "ERROR")
        return False


def install_requirements() -> bool:
    """Instalar dependencias del backend"""
    python_exe = get_python_exe()
    req_file = BACKEND_DIR / "requirements-windows.txt"
    
    if not req_file.exists():
        log(f"Archivo de requisitos no encontrado: {req_file}", "ERROR")
        return False
    
    log(f"Instalando dependencias desde {req_file.name}...")
    try:
        subprocess.run(
            [str(python_exe), "-m", "pip", "install", "--prefer-binary", "-r", str(req_file)],
            cwd=str(BACKEND_DIR),
            check=True,
            capture_output=True
        )
        log("Dependencias instaladas")
        return True
    except subprocess.CalledProcessError as e:
        log(f"Error instalando dependencias: {e}", "ERROR")
        return False


def create_env_file() -> bool:
    """Crear archivo .env con configuración SQLite"""
    if ENV_FILE.exists():
        log(f"Archivo .env ya existe")
        return True
    
    log("Creando archivo .env...")
    env_content = """DEBUG=True
SECRET_KEY=django-insecure-metriclab-dev-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_ALL_ORIGINS=False
"""
    
    try:
        ENV_FILE.write_text(env_content)
        log("Archivo .env creado")
        return True
    except Exception as e:
        log(f"Error creando .env: {e}", "ERROR")
        return False


def run_migrations() -> bool:
    """Ejecutar migraciones de Django"""
    python_exe = get_python_exe()
    log("Ejecutando migraciones de Django...")
    
    try:
        result = subprocess.run(
            [str(python_exe), "manage.py", "migrate", "--noinput"],
            cwd=str(BACKEND_DIR),
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            log(f"Error en migraciones: {result.stderr}", "ERROR")
            return False
        
        log("Migraciones completadas")
        return True
    except Exception as e:
        log(f"Error ejecutando migraciones: {e}", "ERROR")
        return False


def start_backend() -> Optional[subprocess.Popen]:
    """Iniciar servidor Django en background"""
    python_exe = get_python_exe()
    
    if not check_port_available(8000):
        log("Puerto 8000 ya está en uso", "WARNING")
    
    log("Iniciando servidor Django en puerto 8000...")
    
    try:
        process = subprocess.Popen(
            [str(python_exe), "manage.py", "runserver", "0.0.0.0:8000"],
            cwd=str(BACKEND_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
        )
        
        time.sleep(2)  # Esperar a que el servidor inicie
        log("Servidor Django iniciado (PID: {})".format(process.pid))
        return process
        
    except Exception as e:
        log(f"Error iniciando Django: {e}", "ERROR")
        return None


def start_frontend() -> Optional[subprocess.Popen]:
    """Iniciar servidor React en background (si npm está disponible)"""
    if not check_npm_installed():
        log("npm no instalado - frontend no se inicia", "WARNING")
        return None
    
    if not FRONTEND_DIR.exists():
        log(f"Directorio frontend no encontrado: {FRONTEND_DIR}", "ERROR")
        return None
    
    # Verificar si node_modules existe
    node_modules = FRONTEND_DIR / "node_modules"
    if not node_modules.exists():
        log("Instalando dependencias del frontend...")
        try:
            subprocess.run(
                ["npm", "install"],
                cwd=str(FRONTEND_DIR),
                check=True,
                capture_output=True
            )
            log("Dependencias del frontend instaladas")
        except subprocess.CalledProcessError as e:
            log(f"Error instalando dependencias del frontend: {e}", "ERROR")
            return None
    
    if not check_port_available(3000):
        log("Puerto 3000 ya está en uso", "WARNING")
    
    log("Iniciando servidor React en puerto 3000...")
    
    try:
        process = subprocess.Popen(
            ["npm", "start"],
            cwd=str(FRONTEND_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
        )
        
        time.sleep(3)  # Esperar a que React inicie
        log("Servidor React iniciado (PID: {})".format(process.pid))
        return process
        
    except Exception as e:
        log(f"Error iniciando React: {e}", "ERROR")
        return None


def check_npm_installed() -> bool:
    """Verificar si npm está instalado"""
    try:
        subprocess.run(
            ["npm", "--version"],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_backend_status() -> Tuple[bool, str]:
    """Verificar si el backend está disponible"""
    try:
        import requests
        response = requests.get("http://localhost:8000/api/", timeout=2)
        return response.status_code < 500, f"Backend: {response.status_code}"
    except Exception as e:
        return False, "Backend: No disponible"


def get_frontend_status() -> Tuple[bool, str]:
    """Verificar si el frontend está disponible"""
    try:
        import requests
        response = requests.get("http://localhost:3000", timeout=2)
        return response.status_code < 500, f"Frontend: {response.status_code}"
    except Exception as e:
        return False, "Frontend: No disponible"


def show_status(backend_proc: Optional[subprocess.Popen], frontend_proc: Optional[subprocess.Popen]):
    """Mostrar estado de la aplicación"""
    print("\n" + "="*60)
    print("        METRICLAB - ESTADO DE LA APLICACIÓN")
    print("="*60)
    
    backend_running = backend_proc is not None and backend_proc.poll() is None
    frontend_running = frontend_proc is not None and frontend_proc.poll() is None
    
    print(f"\nBackend (Django):")
    print(f"  Estado: {'✓ Ejecutándose' if backend_running else '✗ Detenido'}")
    print(f"  URL: http://localhost:8000")
    print(f"  API: http://localhost:8000/api")
    
    print(f"\nFrontend (React):")
    if frontend_proc is not None:
        print(f"  Estado: {'✓ Ejecutándose' if frontend_running else '✗ Detenido'}")
        print(f"  URL: http://localhost:3000")
    else:
        print(f"  Estado: ⚠ npm no disponible")
    
    print("\n" + "="*60)
    print("Presiona Ctrl+C para detener la aplicación")
    print("="*60 + "\n")


def main():
    """Función principal"""
    print("\n" + "="*60)
    print("   MetricLab - Inicializador para Windows")
    print("="*60 + "\n")
    
    log(f"Directorio raíz: {PROJECT_ROOT}")
    
    # Paso 1: Crear venv
    if not create_venv():
        log("No se pudo crear el entorno virtual", "ERROR")
        sys.exit(1)
    
    # Paso 2: Actualizar pip
    if not upgrade_pip():
        log("No se pudo actualizar pip", "ERROR")
        sys.exit(1)
    
    # Paso 3: Instalar requisitos
    if not install_requirements():
        log("No se pudo instalar las dependencias", "ERROR")
        sys.exit(1)
    
    # Paso 4: Crear .env
    if not create_env_file():
        log("No se pudo crear el archivo .env", "ERROR")
        sys.exit(1)
    
    # Paso 5: Ejecutar migraciones
    if not run_migrations():
        log("Las migraciones no se completaron", "ERROR")
        sys.exit(1)
    
    # Paso 6: Iniciar backend
    backend_proc = start_backend()
    if backend_proc is None:
        log("No se pudo iniciar el backend", "ERROR")
        sys.exit(1)
    
    # Paso 7: Iniciar frontend (opcional)
    frontend_proc = None
    if check_npm_installed():
        frontend_proc = start_frontend()
    
    # Mostrar estado
    show_status(backend_proc, frontend_proc)
    
    try:
        # Mantener los procesos activos
        while True:
            time.sleep(1)
            
            # Verificar si los procesos siguen ejecutándose
            if backend_proc and backend_proc.poll() is not None:
                log("El proceso backend se ha detenido", "ERROR")
                break
            
            if frontend_proc and frontend_proc.poll() is not None:
                log("El proceso frontend se ha detenido", "WARNING")
                frontend_proc = None
    
    except KeyboardInterrupt:
        print("\n")
        log("Deteniendo MetricLab...")
        
        if backend_proc:
            backend_proc.terminate()
            try:
                backend_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                backend_proc.kill()
        
        if frontend_proc:
            frontend_proc.terminate()
            try:
                frontend_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                frontend_proc.kill()
        
        log("MetricLab detenido")
        sys.exit(0)


if __name__ == "__main__":
    main()
