# Backend Django - Time Tracker

## Setup

1. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate
```

2. **Instalar dependencias**
- Para Windows local: `pip install --prefer-binary -r requirements-windows.txt`
- Para la instalación completa: `pip install -r requirements.txt`

3. **Configurar variables de entorno**
- El script `run-windows.bat` crea un `.env` local para SQLite si no existe.
- Para uso manual:
```bash
cp .env.example .env
```

4. **Ejecutar migraciones**
```bash
python manage.py migrate
```

5. **Crear superuser**
```bash
python manage.py createsuperuser
```

6. **Iniciar servidor**
```bash
python manage.py runserver
```

El API estará disponible en: `http://localhost:8000/api`

## Estructura

```
backend/
├── config/              # Configuración Django
├── apps/                # Aplicaciones Django
├── utils/               # Utilidades
├── requirements.txt     # Dependencias
├── manage.py            # CLI Django
└── .env.example         # Plantilla de variables
```

## Testing

```bash
pytest
pytest --cov
```
