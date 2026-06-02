#!/bin/bash
# Script de Configuración Inicial del Backend

cd "$(dirname "$0")" || exit 1

echo "🚀 Configurando Backend Django..."

# Crear estructura de aplicaciones
mkdir -p apps/{users,timetracking,activities,reports,analytics}
mkdir -p apps/{users,timetracking,activities,reports,analytics}/migrations
mkdir -p config
mkdir -p utils
mkdir -p migrations

# Crear __init__.py en cada carpeta
touch apps/__init__.py
touch apps/users/__init__.py
touch apps/users/migrations/__init__.py
touch apps/timetracking/__init__.py
touch apps/timetracking/migrations/__init__.py
touch apps/activities/__init__.py
touch apps/activities/migrations/__init__.py
touch apps/reports/__init__.py
touch apps/reports/migrations/__init__.py
touch apps/analytics/__init__.py
touch apps/analytics/migrations/__init__.py
touch utils/__init__.py
touch config/__init__.py

# Crear archivos por aplicación
for app in users timetracking activities reports analytics; do
    touch apps/$app/models.py
    touch apps/$app/serializers.py
    touch apps/$app/views.py
    touch apps/$app/urls.py
    touch apps/$app/tests.py
    touch apps/$app/admin.py
    touch apps/$app/apps.py
done

# Crear archivos de utilidad
touch utils/decorators.py
touch utils/middleware.py
touch utils/helpers.py

# Crear archivos de configuración
touch config/urls.py
touch config/settings.py
touch config/wsgi.py
touch config/asgi.py

echo "✅ Estructura de backend creada"
echo ""
echo "Próximos pasos:"
echo "1. python -m venv venv"
echo "2. source venv/bin/activate"
echo "3. pip install -r requirements.txt"
echo "4. python manage.py migrate"
echo "5. python manage.py runserver"
