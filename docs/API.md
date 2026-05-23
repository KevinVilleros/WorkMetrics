# Documentación de API

## Base URL

```
Development: http://localhost:8000/api
Production: https://api.timetracker.com/api
```

## Autenticación

Todos los endpoints excepto login y register requieren token JWT.

### Headers Requeridos
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

## Endpoints

###  Authentication

#### Login
```
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response: 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "Juan",
    "role": "employee"
  }
}
```

#### Register
```
POST /auth/register
Content-Type: application/json

{
  "email": "newuser@example.com",
  "password": "password123",
  "first_name": "Juan",
  "last_name": "Pérez"
}

Response: 201 Created
{
  "id": 2,
  "email": "newuser@example.com",
  "name": "Juan Pérez",
  "role": "employee"
}
```

#### Refresh Token
```
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response: 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### ⏱️ Time Tracking

#### Iniciar Tracking
```
POST /tracking/start
Authorization: Bearer <token>
Content-Type: application/json

{
  "project_id": 1,
  "description": "Desarrollo de nueva feature"
}

Response: 201 Created
{
  "entry_id": 123,
  "started_at": "2026-05-21T09:30:00Z",
  "status": "running"
}
```

#### Detener Tracking
```
POST /tracking/stop
Authorization: Bearer <token>

Response: 200 OK
{
  "entry_id": 123,
  "started_at": "2026-05-21T09:30:00Z",
  "ended_at": "2026-05-21T11:35:00Z",
  "duration_minutes": 125,
  "productive_minutes": 106,
  "idle_minutes": 19,
  "efficiency_percentage": 84.8
}
```

#### Pausar Tracking
```
POST /tracking/pause
Authorization: Bearer <token>

Response: 200 OK
{
  "entry_id": 123,
  "status": "paused",
  "paused_at": "2026-05-21T10:30:00Z"
}
```

#### Reanudar Tracking
```
POST /tracking/resume
Authorization: Bearer <token>

Response: 200 OK
{
  "entry_id": 123,
  "status": "running",
  "resumed_at": "2026-05-21T10:35:00Z"
}
```

#### Estado Actual
```
GET /tracking/current
Authorization: Bearer <token>

Response: 200 OK
{
  "entry_id": 123,
  "project": {
    "id": 1,
    "name": "ProjectX"
  },
  "started_at": "2026-05-21T09:30:00Z",
  "elapsed_minutes": 65,
  "status": "running"
}
```

#### Historial de Tracking
```
GET /tracking/history?date=2026-05-21
Authorization: Bearer <token>

Response: 200 OK
{
  "date": "2026-05-21",
  "entries": [
    {
      "id": 123,
      "project": "ProjectX",
      "started_at": "2026-05-21T09:30:00Z",
      "ended_at": "2026-05-21T11:35:00Z",
      "duration_minutes": 125,
      "efficiency_percentage": 84.8
    }
  ]
}
```

###  Reports

#### Reporte Diario
```
GET /reports/daily?date=2026-05-21&user_id=1
Authorization: Bearer <token>

Response: 200 OK
{
  "date": "2026-05-21",
  "user": {
    "id": 1,
    "name": "Juan Pérez"
  },
  "summary": {
    "total_hours": 8.5,
    "productive_hours": 7.2,
    "idle_hours": 1.3,
    "efficiency_percentage": 84.7,
    "breaks_taken": 3,
    "total_entries": 4
  },
  "breakdown": {
    "coding": {
      "minutes": 280,
      "percentage": 54.9
    },
    "meetings": {
      "minutes": 45,
      "percentage": 8.8
    },
    "email": {
      "minutes": 30,
      "percentage": 5.9
    },
    "browsing": {
      "minutes": 75,
      "percentage": 14.7
    },
    "idle": {
      "minutes": 80,
      "percentage": 15.7
    }
  },
  "entries": [
    {
      "id": 123,
      "project": "ProjectX",
      "start_time": "2026-05-21T09:30:00Z",
      "end_time": "2026-05-21T11:35:00Z",
      "duration_minutes": 125,
      "efficiency_percentage": 85.5
    }
  ]
}
```

#### Reporte Semanal
```
GET /reports/weekly?week=2026-05-21&user_id=1
Authorization: Bearer <token>

Response: 200 OK
{
  "week_start": "2026-05-19",
  "week_end": "2026-05-25",
  "summary": {
    "total_hours": 40.5,
    "productive_hours": 34.2,
    "idle_hours": 6.3,
    "average_efficiency": 84.4
  },
  "daily_breakdown": [
    {
      "date": "2026-05-21",
      "total_hours": 8.5,
      "efficiency": 84.7
    }
  ]
}
```

#### Reporte Mensual
```
GET /reports/monthly?month=2026-05&user_id=1
Authorization: Bearer <token>

Response: 200 OK
{
  "month": "2026-05",
  "summary": {
    "total_hours": 162.0,
    "productive_hours": 137.0,
    "idle_hours": 25.0,
    "average_efficiency": 84.6
  },
  "trends": {
    "best_day": "2026-05-22",
    "best_efficiency": 87.2,
    "worst_day": "2026-05-18",
    "worst_efficiency": 79.5
  }
}
```

###  Analytics

#### Eficiencia General
```
GET /analytics/efficiency?start_date=2026-05-01&end_date=2026-05-31
Authorization: Bearer <token>

Response: 200 OK
{
  "period": {
    "start": "2026-05-01",
    "end": "2026-05-31"
  },
  "user_efficiency": 84.6,
  "team_average": 82.3,
  "rank_position": 3,
  "rank_total": 15,
  "comparison_vs_previous_month": "+2.3%"
}
```

#### Desglose de Actividades
```
GET /analytics/breakdown?date=2026-05-21
Authorization: Bearer <token>

Response: 200 OK
{
  "date": "2026-05-21",
  "activities": [
    {
      "type": "coding",
      "percentage": 54.9,
      "minutes": 280,
      "applications": ["VSCode", "Terminal"]
    },
    {
      "type": "meetings",
      "percentage": 8.8,
      "minutes": 45,
      "applications": ["Zoom", "Teams"]
    }
  ]
}
```

###  Users (Admin/Manager)

#### Listar Usuarios
```
GET /users?page=1&limit=20
Authorization: Bearer <token>

Response: 200 OK
{
  "count": 45,
  "next": "http://localhost:8000/api/users?page=2",
  "results": [
    {
      "id": 1,
      "email": "juan@example.com",
      "name": "Juan Pérez",
      "role": "employee",
      "department": "Engineering",
      "last_activity": "2026-05-21T14:30:00Z"
    }
  ]
}
```

#### Obtener Usuario
```
GET /users/:id
Authorization: Bearer <token>

Response: 200 OK
{
  "id": 1,
  "email": "juan@example.com",
  "name": "Juan Pérez",
  "role": "employee",
  "department": "Engineering",
  "manager_id": 5,
  "created_at": "2026-01-15T10:00:00Z"
}
```

#### Crear Usuario (Admin only)
```
POST /users
Authorization: Bearer <token>

{
  "email": "newuser@example.com",
  "first_name": "New",
  "last_name": "User",
  "role": "employee",
  "department": "Engineering",
  "manager_id": 5
}

Response: 201 Created
{
  "id": 50,
  "email": "newuser@example.com",
  "name": "New User",
  "role": "employee"
}
```

## Códigos de Error

| Código | Descripción |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - Token inválido/expirado |
| 403 | Forbidden - Permiso denegado |
| 404 | Not Found - Recurso no encontrado |
| 409 | Conflict - Recurso duplicado |
| 429 | Too Many Requests - Rate limit excedido |
| 500 | Internal Server Error - Error del servidor |

## Rate Limiting

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1613652000
```

---

**Versión API**: 1.0  
**Última Actualización**: 21 de Mayo de 2026
