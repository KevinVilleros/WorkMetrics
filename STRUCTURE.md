#  Estructura Completa del Proyecto

```
Sec-0,1-bet/
│
├──  DOCUMENTACIÓN RAÍZ
│   ├── README.md                 # Descripción general del proyecto
│   ├── ARQUITECTURA.md           # Diseño del sistema
│   ├── ESPECIFICACIONES.md       # Requerimientos técnicos
│   ├── docker-compose.yml        # Orquestación de servicios
│   ├── .gitignore                # Configuración de Git
│   └── setup.sh                  # Script de inicialización
│
├──  docs/                      # Documentación del proyecto
│   ├── API.md                    # Documentación de endpoints
│   ├── DATABASE.md               # Configuración de BD
│   ├── DESARROLLO.md             # Guía de desarrollo local
│   ├── CONTRIBUTING.md           # Guía de contribución
│   ├── MAINTENANCE.md            # Operaciones y mantenimiento
│   ├── ROADMAP.md                # Plan de desarrollo
│   └── ISSUE_TEMPLATE.md         # Plantilla para issues
│
├── ️ .config/                   # Configuración
│   └── nginx.conf                # Configuración de Nginx
│
├──  backend/                   # API REST (Django)
│   ├── config/                   # Configuración Django
│   │   ├── __init__.py
│   │   ├── settings.py           # Settings de Django
│   │   ├── urls.py               # Rutas principales
│   │   ├── wsgi.py               # WSGI application
│   │   └── asgi.py               # ASGI application
│   │
│   ├── apps/                     # Aplicaciones Django
│   │   ├── users/                # Gestión de usuarios
│   │   │   ├── models.py         # Modelos de usuario
│   │   │   ├── serializers.py    # Serializers DRF
│   │   │   ├── views.py          # ViewSets
│   │   │   ├── urls.py           # Rutas de app
│   │   │   ├── admin.py          # Admin Django
│   │   │   ├── tests.py          # Tests
│   │   │   └── migrations/
│   │   │
│   │   ├── timetracking/         # Tracking de tiempo
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── admin.py
│   │   │   ├── tests.py
│   │   │   ├── signals.py        # Señales Django
│   │   │   └── migrations/
│   │   │
│   │   ├── activities/           # Registro de actividades
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── tests.py
│   │   │   └── migrations/
│   │   │
│   │   ├── reports/              # Generación de reportes
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── services.py       # Lógica de negocio
│   │   │   ├── tasks.py          # Celery tasks
│   │   │   ├── tests.py
│   │   │   └── migrations/
│   │   │
│   │   └── analytics/            # Análisis de datos
│   │       ├── views.py
│   │       ├── urls.py
│   │       ├── services.py
│   │       └── tests.py
│   │
│   ├── utils/                    # Utilidades compartidas
│   │   ├── decorators.py         # Decorators personalizados
│   │   ├── middleware.py         # Middlewares
│   │   ├── helpers.py            # Funciones de ayuda
│   │   ├── validators.py         # Validadores
│   │   ├── permissions.py        # Permisos personalizados
│   │   └── exceptions.py         # Excepciones custom
│   │
│   ├── README.md                 # Documentación backend
│   ├── requirements.txt           # Dependencias Python
│   ├── .env.example               # Variables de entorno ejemplo
│   ├── manage.py                  # CLI Django
│   ├── Dockerfile                 # Docker image
│   ├── setup_apps.sh              # Script para crear apps
│   └── pytest.ini                 # Configuración pytest
│
├── ️ frontend/                  # Cliente React
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard/         # Componente Dashboard
│   │   │   ├── Auth/              # Componentes autenticación
│   │   │   ├── TimeTracker/       # Componente tracking
│   │   │   ├── Reports/           # Componente reportes
│   │   │   ├── Charts/            # Gráficos reutilizables
│   │   │   ├── Navbar/            # Barra de navegación
│   │   │   └── Sidebar/           # Barra lateral
│   │   │
│   │   ├── pages/
│   │   │   ├── HomePage.js        # Home
│   │   │   ├── DashboardPage.js   # Dashboard principal
│   │   │   ├── ReportsPage.js     # Página de reportes
│   │   │   ├── SettingsPage.js    # Configuración
│   │   │   └── NotFoundPage.js    # 404
│   │   │
│   │   ├── services/
│   │   │   ├── api.js             # Configuración Axios
│   │   │   ├── authService.js     # Servicios de auth
│   │   │   ├── timeService.js     # Servicios de tracking
│   │   │   ├── reportService.js   # Servicios de reportes
│   │   │   └── analyticsService.js
│   │   │
│   │   ├── redux/
│   │   │   ├── slices/
│   │   │   │   ├── authSlice.js   # Estado de autenticación
│   │   │   │   ├── userSlice.js   # Estado de usuario
│   │   │   │   ├── timeSlice.js   # Estado de tracking
│   │   │   │   └── reportSlice.js # Estado de reportes
│   │   │   ├── store.js           # Configuración Redux
│   │   │   └── hooks.js           # Custom hooks
│   │   │
│   │   ├── utils/
│   │   │   ├── constants.js       # Constantes globales
│   │   │   ├── helpers.js         # Funciones auxiliares
│   │   │   └── validators.js      # Validadores
│   │   │
│   │   ├── styles/
│   │   │   ├── index.css
│   │   │   ├── tailwind.css
│   │   │   └── variables.css      # Variables CSS
│   │   │
│   │   ├── hooks/
│   │   │   ├── useTimer.js        # Hook para temporizador
│   │   │   ├── useAuth.js         # Hook de autenticación
│   │   │   └── useApi.js          # Hook para API
│   │   │
│   │   ├── contexts/
│   │   │   ├── AuthContext.js     # Contexto de autenticación
│   │   │   └── NotificationContext.js
│   │   │
│   │   ├── App.js                 # Componente principal
│   │   ├── index.js               # Entry point
│   │   └── index.css              # Estilos globales
│   │
│   ├── public/
│   │   ├── index.html             # HTML template
│   │   ├── favicon.ico
│   │   └── manifest.json          # PWA manifest
│   │
│   ├── README.md                  # Documentación frontend
│   ├── package.json               # Dependencias Node
│   ├── .env.example               # Variables de entorno ejemplo
│   ├── Dockerfile                 # Docker image
│   ├── setup_dirs.sh              # Script para crear directorios
│   ├── .eslintrc.json             # ESLint config
│   ├── .prettierrc                # Prettier config
│   └── DEPENDENCIES.md            # Lista de dependencias
│
└── ️ logs/                       # Directorio de logs
    └── (generado en runtime)

```

## Estadísticas del Proyecto

- **Aplicaciones Django**: 5 (users, timetracking, activities, reports, analytics)
- **Componentes React**: 10+
- **Documentos**: 10+
- **Archivos de Configuración**: 8+

## Próximos Pasos

1. **Backend**:
   ```bash
   cd backend
   bash setup_apps.sh
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Frontend**:
   ```bash
   cd frontend
   bash setup_dirs.sh
   npm install
   ```

3. **Docker**:
   ```bash
   docker-compose up -d
   ```

---

**Proyecto iniciado**: 21 de Mayo de 2026
