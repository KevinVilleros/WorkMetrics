#!/bin/bash

# Script para inicializar el proyecto

echo "🚀 Inicializando Sistema de Monitoreo de Eficiencia Laboral"

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p backend/apps/{users,timetracking,activities,reports,analytics}
mkdir -p frontend/src/{components,pages,services,redux/slices,styles,utils}
mkdir -p logs

# Backend setup
echo "⚙️  Configurando Backend..."
cd backend
python -m venv venv
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate
pip install --upgrade pip
# pip install -r requirements.txt (cuando exista)
cd ..

# Frontend setup
echo "📦 Configurando Frontend..."
cd frontend
# npm install (cuando se configure)
cd ..

# Docker setup
echo "🐳 Levantando servicios con Docker..."
docker-compose up -d

echo "✅ Inicialización completada"
echo ""
echo "📊 Dashboard: http://localhost:3000"
echo "🔌 API: http://localhost:8000/api"
echo "📋 Admin: http://localhost:8000/admin"
echo ""
echo "Para más información, ver: README.md"
