#!/bin/bash

# Script para inicializar el repositorio Git localmente
# Uso: bash initialize-git.sh

set -e

echo "🚀 Inicializando repositorio Git profesional..."
echo ""

# Verificar si git ya está inicializado
if [ -d .git ]; then
    echo "✅ Repositorio git ya existe"
else
    echo "📝 Inicializando nuevo repositorio..."
    git init
fi

# Configurar usuario global (si es primera vez)
if [ -z "$(git config --global user.name)" ]; then
    echo ""
    echo "⚙️  Configurando usuario git..."
    read -p "Ingresa tu nombre: " GIT_NAME
    read -p "Ingresa tu email: " GIT_EMAIL
    
    git config --global user.name "$GIT_NAME"
    git config --global user.email "$GIT_EMAIL"
    echo "✅ Usuario configurado: $GIT_NAME <$GIT_EMAIL>"
else
    GIT_NAME=$(git config --global user.name)
    GIT_EMAIL=$(git config --global user.email)
    echo "✅ Usando usuario: $GIT_NAME <$GIT_EMAIL>"
fi

# Configurar template de commits
echo ""
echo "📝 Configurando template de commits..."
git config commit.template .gitmessage
echo "✅ Template de commits configurado"

# Configurar alias útiles
echo ""
echo "🔧 Configurando alias de git..."
git config --local alias.co checkout
git config --local alias.br branch
git config --local alias.ci commit
git config --local alias.st status
git config --local alias.visual "log --graph --oneline --all"
git config --local alias.logs "log --oneline --all --graph --decorate"
echo "✅ Alias configurados"

# Hacer add inicial
echo ""
echo "📦 Agregando archivos..."
git add .

# Commit inicial
echo ""
echo "💾 Creando commit inicial..."
git commit -m "chore: proyecto inicial - estructura profesional

Stack: Django + React + PostgreSQL
- Documentación completa
- GitHub Actions CI/CD
- Docker setup
- Tests framework
- Seguridad implementada
- Git workflow profesional" || echo "ℹ️  Los archivos ya estaban commiteados"

# Crear rama develop
echo ""
echo "🌿 Creando rama develop..."
if git show-ref --quiet refs/heads/develop; then
    echo "ℹ️  Rama develop ya existe"
else
    git checkout -b develop
    echo "✅ Rama develop creada"
    git checkout main
fi

# Mostrar resumen
echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ Repositorio Git inicializado correctamente"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📊 Estado actual:"
git status --short | head -20
echo ""
echo "🔗 Ramas locales:"
git branch -v
echo ""
echo "📝 Commits recientes:"
git log --oneline -5
echo ""
echo "════════════════════════════════════════════════════════════"
echo "🚀 Próximos pasos:"
echo ""
echo "1️⃣  Crear repositorio en GitHub (PRIVADO)"
echo "   → https://github.com/new"
echo ""
echo "2️⃣  Conectar repositorio remoto:"
echo "   → git remote add origin https://github.com/TU_USUARIO/Sec-0,1-bet.git"
echo ""
echo "3️⃣  Hacer push del código:"
echo "   → git push -u origin main"
echo "   → git push -u origin develop"
echo ""
echo "4️⃣  Configurar protecciones de ramas en GitHub"
echo "   → Ver: GITHUB_SETUP.md (Paso 4)"
echo ""
echo "5️⃣  Configurar secretos y CI/CD"
echo "   → Ver: GITHUB_SETUP.md (Paso 5)"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📖 Para más detalles, consulta: GITHUB_SETUP.md"
echo ""
