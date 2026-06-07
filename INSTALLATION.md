# 📦 Guía de Instalación - MetricLab

## Requisitos del Sistema

### Windows
- **Windows 10/11** (64-bit)
- **Python 3.10+** (https://www.python.org/downloads/)
- **Node.js 16+** (https://nodejs.org/)
- **PostgreSQL 13+** (opcional, se puede usar SQLite)
- **4GB RAM mínimo, 8GB recomendado**

### Linux (Ubuntu/Debian)
- **Ubuntu 20.04+** o **Debian 10+**
- **Python 3.10+** (generalmente preinstalado)
- **Node.js 16+**
- **PostgreSQL 13+** (opcional)
- **4GB RAM mínimo**

### macOS
- **macOS 10.14+**
- Seguir procedimiento similar a Linux

---

## 🚀 Instalación Rápida

### Windows

1. **Descargar el instalador**
   - Descarga `install-windows.bat` desde el repositorio
   - O desde las [Releases](https://github.com/KevinVilleros/WorkMetrics/releases)

2. **Ejecutar instalador**
   ```bash
   install-windows.bat
   ```
   - Se instalará automáticamente en: `C:\Users\{Usuario}\AppData\Roaming\MetricLab`

3. **Iniciar la aplicación**
   - Opción 1: Busca "MetricLab" en el menú Inicio
   - Opción 2: Ejecuta: `C:\Users\{Usuario}\AppData\Roaming\MetricLab\start-metriclab.bat`

### Linux

1. **Descargar el instalador**
   ```bash
   wget https://raw.githubusercontent.com/KevinVilleros/WorkMetrics/main/install-linux.sh
   chmod +x install-linux.sh
   ```

2. **Ejecutar instalador**
   ```bash
   bash install-linux.sh
   ```
   - Se instalará en: `$HOME/.metriclab`

3. **Iniciar la aplicación**
   ```bash
   bash ~/.metriclab/start-metriclab.sh
   ```

---

## 🐳 Instalación con Docker (Recomendado para Producción)

### Requisitos
- Docker 20.10+
- Docker Compose 2.0+

### Pasos

1. **Clonar repositorio**
   ```bash
   git clone https://github.com/KevinVilleros/WorkMetrics.git
   cd WorkMetrics
   ```

2. **Crear archivo `.env`**
   ```bash
   cp backend/.env.example backend/.env
   ```

3. **Editar configuración** (opcional)
   ```bash
   nano backend/.env
   ```

4. **Iniciar con Docker Compose**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

5. **Ejecutar migraciones**
   ```bash
   docker exec metriclab_backend python manage.py migrate
   ```

6. **Acceder a la aplicación**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Nginx: http://localhost

---

## 📝 Instalación Manual

Si prefieres instalar manualmente:

### Windows

```bash
# 1. Clonar repositorio
git clone https://github.com/KevinVilleros/WorkMetrics.git
cd WorkMetrics

# 2. Backend
cd backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000

# 3. Frontend (en otra terminal)
cd frontend
npm install
npm start
```

### Linux/macOS

```bash
# 1. Clonar repositorio
git clone https://github.com/KevinVilleros/WorkMetrics.git
cd WorkMetrics

# 2. Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000

# 3. Frontend (en otra terminal)
cd frontend
npm install
npm start
```

---

## 🔧 Configuración

### Variables de Entorno (`.env`)

**Backend** - `backend/.env`:
```env
DEBUG=False
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/metriclab
ALLOWED_HOSTS=localhost,127.0.0.1,tu-dominio.com
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

**Frontend** - `frontend/.env`:
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_ENV=production
```

---

## 📊 Acceso a la Aplicación

Una vez instalada, accede a:

| Componente | URL | Usuario Predeterminado |
|-----------|-----|----------------------|
| Frontend | http://localhost:3000 | demo@metriclab.com / demo123 |
| Backend API | http://localhost:8000 | N/A |
| Admin | http://localhost:8000/admin | admin / admin |
| Docs API | http://localhost:8000/api/docs | N/A |

---

## 🛑 Detener la Aplicación

### Windows
```bash
# Opción 1: Cerrar las ventanas de consola
# Opción 2: Ejecutar
stop-metriclab.bat
```

### Linux
```bash
bash ~/.metriclab/stop-metriclab.sh
```

### Docker
```bash
docker-compose -f docker-compose.prod.yml down
```

---

## 🐛 Troubleshooting

### Error: "Python not found"
- Asegúrate de que Python está instalado: `python --version`
- En Linux/macOS usa: `python3 --version`

### Error: "Port 8000 already in use"
- Cambia el puerto en el comando: `python manage.py runserver 8001`

### Error: "Cannot find npm"
- Instala Node.js desde: https://nodejs.org/

### Error: "PostgreSQL connection refused"
- Asegúrate de que PostgreSQL está corriendo
- O usa SQLite editando `backend/.env`

### Error: "CORS policy error"
- Verifica la configuración de CORS_ALLOWED_ORIGINS en `backend/.env`

---

## 📋 Instalación desde Releases (Ejecutables Pre-compilados)

1. Ve a: https://github.com/KevinVilleros/WorkMetrics/releases
2. Descarga el archivo apropiado:
   - `metriclab-windows-v1.0.0.zip` para Windows
   - `metriclab-linux-v1.0.0.tar.gz` para Linux
3. Extrae el archivo
4. Lee las instrucciones en el archivo `README.txt` incluido

---

## 📞 Soporte

Para problemas o preguntas:
- 📧 Email: support@metriclab.com
- 🐛 Issues: https://github.com/KevinVilleros/WorkMetrics/issues
- 💬 Discussions: https://github.com/KevinVilleros/WorkMetrics/discussions

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver [LICENSE](LICENSE) para más detalles.
