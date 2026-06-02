#!/bin/bash
# Script de Configuración Inicial del Frontend

cd "$(dirname "$0")" || exit 1

echo "🎨 Configurando Frontend React..."

# Crear estructura de directorios
mkdir -p src/{components,pages,services,redux/slices,styles,utils,hooks,contexts}

# Crear subdirectorios de componentes
mkdir -p src/components/{Dashboard,Auth,TimeTracker,Reports,Navbar,Sidebar,Charts}

# Crear archivos iniciales
touch src/index.js
touch src/App.js
touch src/App.css
touch src/index.css

# Components
touch src/components/Dashboard/Dashboard.js
touch src/components/Auth/Login.js
touch src/components/Auth/Register.js
touch src/components/TimeTracker/TimeTracker.js
touch src/components/Reports/ReportView.js
touch src/components/Navbar/Navbar.js
touch src/components/Sidebar/Sidebar.js

# Pages
touch src/pages/HomePage.js
touch src/pages/DashboardPage.js
touch src/pages/ReportsPage.js
touch src/pages/SettingsPage.js

# Services
touch src/services/api.js
touch src/services/authService.js
touch src/services/timeService.js
touch src/services/reportService.js

# Redux
touch src/redux/store.js
touch src/redux/hooks.js
touch src/redux/slices/authSlice.js
touch src/redux/slices/userSlice.js
touch src/redux/slices/timeSlice.js

# Utils
touch src/utils/constants.js
touch src/utils/helpers.js
touch src/utils/validators.js

# Styles
touch src/styles/variables.css
touch src/styles/tailwind.css

echo "✅ Estructura de frontend creada"
echo ""
echo "Próximos pasos:"
echo "1. npm install"
echo "2. npm start"
