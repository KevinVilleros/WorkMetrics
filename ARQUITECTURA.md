# ️ Arquitectura del Sistema

## Visión General

Sistema de arquitectura de 3 capas con API REST, implementando patrones de desarrollo profesional y escalable.

```
┌─────────────────────────────────────────────────────────────┐
│                     CAPA DE PRESENTACIÓN                     │
│                 React Frontend (Single Page App)             │
│                   Dashboard & UI Components                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTP/REST
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                  CAPA DE NEGOCIO (API)                       │
│              Django REST Framework Backend                   │
│        ├─ Authentication & Authorization                    │
│        ├─ Business Logic                                    │
│        ├─ Data Processing                                   │
│        └─ Integration Services                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ SQL Queries
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                  CAPA DE DATOS                               │
│              PostgreSQL Database                            │
│        ├─ User Management                                   │
│        ├─ Time Tracking Records                             │
│        ├─ Activity Logs                                     │
│        └─ Reports & Analytics                               │
└─────────────────────────────────────────────────────────────┘
```

## ️ Estructura de Carpetas

### Backend

```
backend/
├── config/                      # Configuración de Django
│   ├── settings.py              # Configuraciones principales
│   ├── urls.py                  # Rutas principales
│   └── wsgi.py                  # WSGI entry point
├── apps/                        # Aplicaciones Django
│   ├── users/                   # Gestión de usuarios
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   ├── timetracking/            # Tracking de tiempo
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   ├── activities/              # Registro de actividades
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── reports/                 # Generación de reportes
│   │   ├── models.py
│   │   ├── services.py
│   │   ├── views.py
│   │   └── urls.py
│   └── analytics/               # Análisis de datos
│       ├── services.py
│       ├── views.py
│       └── urls.py
├── utils/                       # Utilidades comunes
│   ├── decorators.py
│   ├── middleware.py
│   └── helpers.py
├── migrations/                  # Migraciones de BD
├── requirements.txt             # Dependencias
├── manage.py                    # Django CLI
├── .env.example                 # Variables de entorno ejemplo
└── README.md                    # Documentación backend
```

### Frontend

```
frontend/
├── src/
│   ├── components/              # Componentes reutilizables
│   │   ├── Dashboard/
│   │   ├── Navbar/
│   │   ├── Sidebar/
│   │   ├── TimeTracker/
│   │   ├── ReportView/
│   │   └── Charts/
│   ├── pages/                   # Páginas principales
│   │   ├── Home.js
│   │   ├── Login.js
│   │   ├── Dashboard.js
│   │   ├── Reports.js
│   │   ├── Employees.js
│   │   └── NotFound.js
│   ├── services/                # Servicios API
│   │   ├── api.js               # Configuración axios
│   │   ├── authService.js
│   │   ├── timeService.js
│   │   ├── reportService.js
│   │   └── analyticsService.js
│   ├── redux/                   # Redux store
│   │   ├── slices/
│   │   │   ├── authSlice.js
│   │   │   ├── userSlice.js
│   │   │   ├── timeSlice.js
│   │   │   └── reportSlice.js
│   │   ├── store.js
│   │   └── hooks.js
│   ├── styles/                  # Estilos globales
│   │   ├── index.css
│   │   ├── tailwind.css
│   │   └── variables.css
│   ├── utils/                   # Utilidades
│   │   ├── constants.js
│   │   ├── helpers.js
│   │   └── validators.js
│   ├── App.js
│   ├── index.js
│   └── .env.example
├── public/
│   ├── index.html
│   └── favicon.ico
├── package.json
└── README.md
```

##  Modelo de Datos

### Entidades Principales

```
User
├── id (PK)
├── email (UNIQUE)
├── password (encrypted)
├── first_name
├── last_name
├── role (admin/manager/employee)
├── department
├── created_at
├── updated_at
└── is_active

TimeEntry
├── id (PK)
├── user_id (FK)
├── start_time
├── end_time
├── duration_minutes
├── project_id (FK)
├── status (active/paused/completed)
└── created_at

Activity
├── id (PK)
├── time_entry_id (FK)
├── user_id (FK)
├── activity_type (typing/mouse_click/idle)
├── timestamp
├── application (focused app)
└── details (json)

Project
├── id (PK)
├── name
├── description
├── manager_id (FK)
├── created_at
└── is_active

Report
├── id (PK)
├── user_id (FK)
├── report_date
├── total_hours
├── productive_hours
├── idle_hours
├── efficiency_percentage
└── generated_at
```

##  Flujo de Datos

### Timeline del Tracking

```
1. Usuario inicia sesión
   ↓
2. Frontend solicita START_TRACKING
   ↓
3. Backend crea TimeEntry en BD
   ↓
4. Frontend monitorea actividad en cliente
   ↓
5. Cada 30 segundos: envía Activity logs
   ↓
6. Backend procesa y almacena actividades
   ↓
7. Frontend calcula métricas locales
   ↓
8. Usuario detiene tracking o fin de jornada
   ↓
9. Backend calcula eficiencia y genera reporte
```

##  Seguridad

### Autenticación
- JWT tokens con refresh tokens
- Expiración configurable
- Blacklist de tokens revocados

### Autorización
- RBAC (Role-Based Access Control)
- Verificación en decorators/middleware
- Validación de permisos en cada endpoint

### Validación
- Serializers en Django
- Validación frontend
- Rate limiting por IP/usuario

##  API Endpoints Principales

```
AUTH
POST   /api/auth/login              - Autenticación
POST   /api/auth/logout             - Cerrar sesión
POST   /api/auth/refresh            - Refrescar token
POST   /api/auth/register           - Registrarse

TRACKING
POST   /api/tracking/start          - Iniciar tracking
POST   /api/tracking/stop           - Detener tracking
GET    /api/tracking/current        - Estado actual
GET    /api/tracking/history        - Historial

ACTIVITIES
POST   /api/activities/log          - Registrar actividad
GET    /api/activities/report       - Reporte de actividades

REPORTS
GET    /api/reports/daily           - Reporte diario
GET    /api/reports/weekly          - Reporte semanal
GET    /api/reports/monthly         - Reporte mensual
GET    /api/reports/user/:id        - Reporte por usuario

ANALYTICS
GET    /api/analytics/efficiency    - Índice de eficiencia
GET    /api/analytics/breakdown     - Desglose de actividades
GET    /api/analytics/trends        - Tendencias

USERS (Admin/Manager)
GET    /api/users                   - Listar usuarios
POST   /api/users                   - Crear usuario
PUT    /api/users/:id               - Actualizar usuario
DELETE /api/users/:id               - Eliminar usuario
```

##  Ciclo de Despliegue

```
Development → Staging → Production

1. Desarrollo local (venv + npm)
2. Testing automático
3. Docker build
4. Push a registry
5. Despliegue a servidor
6. Monitoreo y logs
```

---

Última actualización: 21 de Mayo de 2026
