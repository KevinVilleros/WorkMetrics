#!/usr/bin/env python
"""
MetricLab Standalone - Sistema de Detección de Personas para Evaluación de Eficiencia Laboral
Ejecutable completo que incluye Backend (Django) + Frontend (React) + Database
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser
import signal
import shutil
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

METRICLAB_HOME = Path.home() / ".metriclab"
BACKEND_PORT = 8000
FRONTEND_PORT = 3000
DB_PATH = METRICLAB_HOME / "db.sqlite3"
VENV_PATH = METRICLAB_HOME / "venv"
LOGS_PATH = METRICLAB_HOME / "logs"

# ============================================================================
# CLASE PRINCIPAL
# ============================================================================

class MetricLabStandalone:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def setup(self):
        """Configurar directorios y base de datos"""
        print("\n[SETUP] Inicializando MetricLab...")
        
        # Crear directorios
        METRICLAB_HOME.mkdir(exist_ok=True)
        LOGS_PATH.mkdir(exist_ok=True)
        
        # Crear .env si no existe
        env_file = METRICLAB_HOME / ".env"
        if not env_file.exists():
            env_content = f"""DEBUG=False
SECRET_KEY={os.urandom(32).hex()}
DATABASE_URL=sqlite:///{DB_PATH}
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:{FRONTEND_PORT}
"""
            env_file.write_text(env_content)
            print(f"✓ Archivo .env creado: {env_file}")
        
        # Crear base de datos inicial
        if not DB_PATH.exists():
            print("✓ Base de datos creada: SQLite")
            DB_PATH.touch()
    
    def create_launcher_script(self):
        """Crear script launcher que inicia todo"""
        launcher_path = METRICLAB_HOME / "launcher.py"
        
        launcher_code = f"""
import subprocess
import sys
import os
import time

backend_dir = os.path.join(r'{Path(__file__).parent}', 'backend')
# Agregar rutas
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

# Variables de entorno
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['PYTHONPATH'] = backend_dir

print("="*60)
print("  MetricLab - Sistema de Detección de Eficiencia Laboral")
print("="*60)
print()

# Iniciar backend
print("[1/2] Iniciando Backend (Django)...")
backend_cmd = [
    sys.executable, '-m', 'django',
    'runserver', '0.0.0.0:{BACKEND_PORT}'
]
backend = subprocess.Popen(backend_cmd)

time.sleep(3)

# Iniciar frontend
print("[2/2] Iniciando Frontend (React)...")
print()
print("✓ Backend: http://localhost:{BACKEND_PORT}")
print("✓ Frontend: http://localhost:{FRONTEND_PORT}")
print()
print("Abriendo en navegador...")

# Abrir en navegador
import webbrowser
webbrowser.open(f'http://localhost:{FRONTEND_PORT}')

try:
    backend.wait()
except KeyboardInterrupt:
    print("\\nCerrando MetricLab...")
    backend.terminate()
    backend.wait()
"""
        launcher_path.write_text(launcher_code)
        return launcher_path
    
    def start_backend(self):
        """Iniciar servidor backend Django"""
        print(f"\n[BACKEND] Iniciando en puerto {BACKEND_PORT}...")
        
        backend_dir = Path(__file__).parent / 'backend'
        cmd = [
            sys.executable, '-m', 'django',
            'runserver', f'0.0.0.0:{BACKEND_PORT}'
        ]
        
        env = os.environ.copy()
        env['DJANGO_SETTINGS_MODULE'] = 'config.settings'
        env['PYTHONUNBUFFERED'] = '1'
        env['PYTHONPATH'] = str(backend_dir)
        
        self.backend_process = subprocess.Popen(
            cmd,
            cwd=backend_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(3)  # Esperar a que inicie
        print(f"✓ Backend ejecutándose: http://localhost:{BACKEND_PORT}")
    
    def start_frontend(self):
        """Iniciar servidor frontend (build estático o producción dev)"""
        print(f"\n[FRONTEND] Iniciando en puerto {FRONTEND_PORT}...")
        
        frontend_dir = Path(__file__).parent / "frontend"
        build_path = frontend_dir / "build"
        
        if build_path.exists():
            # Usar build estático
            cmd = [sys.executable, '-m', 'http.server', str(FRONTEND_PORT)]
            cwd = build_path
        else:
            npm_cmd = shutil.which('npm') or shutil.which('npm.cmd')
            if not npm_cmd:
                raise FileNotFoundError('npm no encontrado. Instala Node.js y asegúrate de que npm esté en PATH.')
            
            node_modules_path = frontend_dir / 'node_modules'
            if not node_modules_path.exists():
                print("[FRONTEND] node_modules no encontrado. Ejecutando npm install...")
                install_cmd = [npm_cmd, 'install']
                install_process = subprocess.Popen(
                    install_cmd,
                    cwd=frontend_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=False
                )
                install_stdout, install_stderr = install_process.communicate()
                if install_process.returncode != 0:
                    print(install_stdout.decode(errors='ignore'))
                    print(install_stderr.decode(errors='ignore'))
                    raise RuntimeError('Falló npm install para el frontend.')

            print("[FRONTEND] No se encontró build. Generando producción con npm run build...")
            build_cmd = [npm_cmd, 'run', 'build']
            build_process = subprocess.Popen(
                build_cmd,
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False
            )
            build_stdout, build_stderr = build_process.communicate()
            if build_process.returncode != 0:
                print(build_stdout.decode(errors='ignore'))
                print(build_stderr.decode(errors='ignore'))
                raise RuntimeError('Falló la compilación del frontend con npm run build.')

            if not build_path.exists():
                raise FileNotFoundError('El build del frontend no se generó correctamente.')

            cmd = [sys.executable, '-m', 'http.server', str(FRONTEND_PORT)]
            cwd = build_path
        
        self.frontend_process = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(2)
        print(f"✓ Frontend ejecutándose: http://localhost:{FRONTEND_PORT}")
    
    def open_browser(self):
        """Abrir navegador en la aplicación"""
        print("\n[NAVEGADOR] Abriendo interfaz gráfica...")
        time.sleep(2)
        webbrowser.open(f'http://localhost:{FRONTEND_PORT}')
    
    def run(self):
        """Ejecutar MetricLab"""
        try:
            self.setup()
            self.start_backend()
            time.sleep(2)
            self.start_frontend()
            self.open_browser()
            
            print("\n" + "="*60)
            print("  MetricLab está ejecutándose")
            print("="*60)
            print()
            print("  📊 Dashboard: http://localhost:3000")
            print("  📡 API Backend: http://localhost:8000/api")
            print("  ⚙️  Admin: http://localhost:8000/admin")
            print()
            print("  Presiona Ctrl+C para detener")
            print("="*60 + "\n")
            
            # Mantener procesos corriendo
            while self.running:
                time.sleep(1)
                if self.backend_process and self.backend_process.poll() is not None:
                    print("[ERROR] Backend se detuvo")
                    break
                if self.frontend_process and self.frontend_process.poll() is not None:
                    print("[ERROR] Frontend se detuvo")
                    break
        
        except KeyboardInterrupt:
            print("\n\n[CIERRE] Deteniendo MetricLab...")
            self.stop()
        except Exception as e:
            print(f"\n[ERROR] {e}")
            self.stop()
    
    def stop(self):
        """Detener todos los procesos"""
        self.running = False
        
        if self.backend_process:
            print("  - Cerrando Backend...")
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except:
                self.backend_process.kill()
        
        if self.frontend_process:
            print("  - Cerrando Frontend...")
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except:
                self.frontend_process.kill()
        
        print("\n✓ MetricLab cerrado correctamente\n")
        sys.exit(0)

# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == '__main__':
    app = MetricLabStandalone()
    
    # Manejar señales
    signal.signal(signal.SIGINT, lambda sig, frame: app.stop())
    signal.signal(signal.SIGTERM, lambda sig, frame: app.stop())
    
    app.run()
