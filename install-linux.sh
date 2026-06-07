#!/bin/bash
# Script de instalación y ejecución para Linux
# Soporta Ubuntu, Debian, Fedora, Arch Linux

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}MetricLab - Sistema de Monitoreo Laboral${NC}"
echo -e "${GREEN}Instalador para Linux${NC}"
echo -e "${GREEN}========================================${NC}\n"

# Detectar distro
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo -e "${RED}No se pudo detectar el sistema operativo${NC}"
    exit 1
fi

echo -e "${YELLOW}Sistema detectado: $OS${NC}"

# Instalar dependencias del sistema
echo -e "\n${YELLOW}[1/5] Instalando dependencias del sistema...${NC}"

case $OS in
    ubuntu|debian)
        sudo apt-get update
        sudo apt-get install -y python3-pip python3-venv python3-dev \
            postgresql postgresql-contrib libpq-dev \
            nodejs npm \
            git build-essential \
            libgl1-mesa-glx libglib2.0-0
        ;;
    fedora)
        sudo dnf install -y python3-pip python3-devel \
            postgresql postgresql-server postgresql-libs postgresql-devel \
            nodejs npm \
            git gcc gcc-c++ \
            mesa-libGL glib2
        ;;
    arch)
        sudo pacman -S --noconfirm python-pip python \
            postgresql \
            nodejs npm \
            git base-devel \
            mesa glib2
        ;;
    *)
        echo -e "${RED}Distro no soportada: $OS${NC}"
        echo -e "${YELLOW}Por favor, instala manualmente: Python3, PostgreSQL, Node.js, npm, git${NC}"
        ;;
esac

# Crear directorio base
APP_DIR="$HOME/.metriclab"
mkdir -p "$APP_DIR"
cd "$APP_DIR"

# Clonar o actualizar repositorio
echo -e "\n${YELLOW}[2/5] Descargando aplicación...${NC}"
if [ -d "WorkMetrics" ]; then
    cd WorkMetrics
    git pull
else
    git clone https://github.com/KevinVilleros/WorkMetrics.git
    cd WorkMetrics
fi

# Backend setup
echo -e "\n${YELLOW}[3/5] Configurando Backend (Python)...${NC}"
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Crear .env si no existe
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}Archivo .env creado. Por favor, edita $APP_DIR/WorkMetrics/backend/.env con tu configuración${NC}"
fi

# Ejecutar migraciones
python manage.py migrate

cd ..

# Frontend setup
echo -e "\n${YELLOW}[4/5] Configurando Frontend (React)...${NC}"
cd frontend
npm install

cd ..

# Crear scripts de ejecución
echo -e "\n${YELLOW}[5/5] Creando scripts de ejecución...${NC}"

# Script para iniciar la aplicación
cat > "$APP_DIR/start-metriclab.sh" << 'EOF'
#!/bin/bash
APP_DIR="$HOME/.metriclab/WorkMetrics"

echo "🚀 Iniciando MetricLab..."
echo ""
echo "⏳ Iniciando Backend (Django)..."
cd "$APP_DIR/backend"
source venv/bin/activate
python manage.py runserver 8000 &
BACKEND_PID=$!

echo "⏳ Iniciando Frontend (React)..."
cd "$APP_DIR/frontend"
npm start &
FRONTEND_PID=$!

echo ""
echo "✅ MetricLab iniciado"
echo "🌐 Frontend: http://localhost:3000"
echo "🔗 Backend API: http://localhost:8000"
echo ""
echo "Presiona Ctrl+C para detener"

wait
EOF

chmod +x "$APP_DIR/start-metriclab.sh"

# Script para detener
cat > "$APP_DIR/stop-metriclab.sh" << 'EOF'
#!/bin/bash
echo "Deteniendo MetricLab..."
pkill -f "python manage.py runserver"
pkill -f "npm start"
pkill -f "react-scripts"
echo "✅ Detenido"
EOF

chmod +x "$APP_DIR/stop-metriclab.sh"

# Crear acceso directo en menú
cat > "$HOME/.local/share/applications/metriclab.desktop" << 'EOF'
[Desktop Entry]
Type=Application
Name=MetricLab
Comment=Sistema de Monitoreo de Eficiencia Laboral
Icon=dialog-information
Exec=bash -c 'source ~/.metriclab/start-metriclab.sh'
Terminal=true
Categories=Productivity;
EOF

chmod +x "$HOME/.local/share/applications/metriclab.desktop"

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Instalación completada${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Para iniciar la aplicación, ejecuta:${NC}"
echo -e "${GREEN}  bash ~/.metriclab/start-metriclab.sh${NC}"
echo ""
echo -e "${YELLOW}O busca 'MetricLab' en el menú de aplicaciones${NC}"
echo ""
echo -e "${YELLOW}Para detener:${NC}"
echo -e "${GREEN}  bash ~/.metriclab/stop-metriclab.sh${NC}"
