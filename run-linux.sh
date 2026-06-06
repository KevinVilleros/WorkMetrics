#!/bin/bash
# Script de ejecución para Linux (después de instalación)

set -e

APP_DIR="$HOME/.metriclab/WorkMetrics"

if [ ! -d "$APP_DIR" ]; then
    echo "❌ MetricLab no está instalado"
    echo "Por favor, ejecuta primero: bash install-linux.sh"
    exit 1
fi

echo ""
echo "🚀 Iniciando MetricLab..."
echo ""

# Iniciar Backend
echo "⏳ Iniciando Backend (Django)..."
cd "$APP_DIR/backend"
source venv/bin/activate
python manage.py runserver 8000 &
BACKEND_PID=$!
echo "✅ Backend iniciado (PID: $BACKEND_PID)"

# Esperar a que el backend esté listo
sleep 3

# Iniciar Frontend
echo "⏳ Iniciando Frontend (React)..."
cd "$APP_DIR/frontend"
npm start &
FRONTEND_PID=$!
echo "✅ Frontend iniciado (PID: $FRONTEND_PID)"

echo ""
echo "==========================================+="
echo "✅ MetricLab iniciado correctamente"
echo "==========================================="
echo ""
echo "🌐 Frontend:  http://localhost:3000"
echo "🔗 Backend:   http://localhost:8000"
echo ""
echo "📝 Presiona Ctrl+C para detener"
echo ""

# Trap para manejar Ctrl+C
trap "
    echo ''
    echo '⏹️  Deteniendo MetricLab...'
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo '✅ Detenido'
    exit 0
" INT TERM

# Esperar a que ambos procesos terminen
wait
