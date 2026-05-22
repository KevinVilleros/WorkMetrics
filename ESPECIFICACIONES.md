










































































































































































































































































































































































































































# 📋 Especificaciones Técnicas

## Versión 1.0 - MVP

**Fecha**: 21 de Mayo de 2026

## 1. Requerimientos Funcionales

### 1.1 Autenticación y Autorización

**RF-001**: Sistema de login seguro
- Registro de usuarios
- Autenticación con JWT
- Recuperación de contraseña
- Validación de email

**RF-002**: Gestión de roles
- Rol Admin: acceso total
- Rol Manager: gestión de equipo
- Rol Empleado: acceso personal
- Control granular de permisos

### 1.2 Tracking de Tiempo

**RF-003**: Sistema de tracking en tiempo real
- Botón START/STOP tracking
- Temporizador visible
- Pausa manual
- Resumen de jornada

**RF-004**: Detección automática de inactividad
- Monitoreo de mouse/teclado
- Detección de inactividad > 5 minutos
- Alerta opcional al usuario
- Registro de tiempo inactivo

### 1.3 Registro de Actividades

**RF-005**: Logging de actividades
- Captura de aplicación activa
- Registro de tecleo
- Movimiento de mouse
- Cambios de ventana/aplicación

**RF-006**: Historial de actividades
- Visualización por fecha
- Filtros por tipo de actividad
- Timeline interactivo
- Exportación de logs

### 1.4 Reportes

**RF-007**: Reportes de eficiencia
- Reporte diario por usuario
- Reporte semanal
- Reporte mensual
- Comparativa periódica

**RF-008**: Análisis de tiempo
- Horas productivas vs inactivas
- Distribución de horas por proyecto
- Identificación de picos de productividad
- Análisis de patrones

**RF-009**: Exportación de reportes
- Exportar a PDF
- Exportar a Excel
- Envío por email
- Programación de reportes automáticos

### 1.5 Dashboard

**RF-010**: Dashboard ejecutivo
- KPIs principales
- Gráficas en tiempo real
- Comparativas de desempeño
- Alertas de bajo desempeño

**RF-011**: Dashboard de empleado
- Mi productividad hoy
- Objetivo vs realidad
- Histórico personal
- Metas establecidas

## 2. Requerimientos No Funcionales

### 2.1 Rendimiento

**RNF-001**: Tiempo de respuesta
- APIs: < 500ms
- Frontend: renderizado < 1s
- Inicialización: < 2s

**RNF-002**: Escalabilidad
- Soportar 1000+ usuarios concurrentes
- BD optimizada con índices
- Caché implementado (Redis)

**RNF-003**: Disponibilidad
- Uptime: 99.5%
- Backup automático
- Recuperación ante fallos

### 2.2 Seguridad

**RNF-004**: Protección de datos
- Encriptación en tránsito (HTTPS)
- Encriptación en reposo (BD)
- Hash de contraseñas con bcrypt
- Rate limiting

**RNF-005**: Auditoría
- Log de todas las acciones
- Registro de cambios
- Trazabilidad completa

### 2.3 Usabilidad

**RNF-006**: Interfaz intuitiva
- Responsive design
- Accesibilidad WCAG 2.1 AA
- Dark mode opcional
- 3 idiomas (ES, EN, PT)

**RNF-007**: Dispositivos
- Desktop (Chrome, Firefox, Safari, Edge)
- Tablet compatible
- Preparado para mobile (v1.2)

## 3. Especificaciones de API

### 3.1 Autenticación

```
POST /api/auth/login
Request:
{
  "email": "user@example.com",
  "password": "password123"
}

Response: 200 OK
{
  "access_token": "jwt_token",
  "refresh_token": "refresh_token",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "employee",
    "name": "Juan"
  }
}
```

### 3.2 Tracking de Tiempo

```
POST /api/tracking/start
Request:
{
  "project_id": 1,
  "description": "Desarrollo de features"
}

Response: 201 Created
{
  "entry_id": 123,
  "started_at": "2026-05-21T09:30:00Z",
  "status": "running"
}

---

POST /api/tracking/stop
Response: 200 OK
{
  "entry_id": 123,
  "duration_minutes": 125,
  "ended_at": "2026-05-21T11:35:00Z",
  "productive_time_percentage": 85.5
}
```

### 3.3 Reportes

```
GET /api/reports/daily?date=2026-05-21&user_id=1
Response: 200 OK
{
  "date": "2026-05-21",
  "user": {
    "id": 1,
    "name": "Juan"
  },
  "summary": {
    "total_hours": 8.5,
    "productive_hours": 7.2,
    "idle_hours": 1.3,
    "efficiency_percentage": 84.7
  },
  "entries": [
    {
      "id": 123,
      "project": "ProjectX",
      "duration_minutes": 125,
      "productive_percentage": 85.5
    }
  ],
  "breakdown": {
    "coding": 280,
    "meetings": 45,
    "email": 30,
    "idle": 75
  }
}
```

## 4. Modelos de Base de Datos

### User (Usuarios)
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  role VARCHAR(20) DEFAULT 'employee',
  department VARCHAR(100),
  manager_id INT REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  is_active BOOLEAN DEFAULT TRUE
);
```

### TimeEntry (Registros de Tiempo)
```sql
CREATE TABLE time_entries (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id),
  project_id INT REFERENCES projects(id),
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP,
  duration_minutes INT,
  productive_minutes INT,
  idle_minutes INT,
  description TEXT,
  status VARCHAR(20) DEFAULT 'active',
  created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_user_date ON time_entries(user_id, start_time);
```

### Activity (Log de Actividades)
```sql
CREATE TABLE activities (
  id SERIAL PRIMARY KEY,
  time_entry_id INT NOT NULL REFERENCES time_entries(id),
  user_id INT NOT NULL REFERENCES users(id),
  activity_type VARCHAR(50),
  application VARCHAR(255),
  active BOOLEAN DEFAULT TRUE,
  captured_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_entry_time ON activities(time_entry_id, captured_at);
```

### Project (Proyectos)
```sql
CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  manager_id INT REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  is_active BOOLEAN DEFAULT TRUE
);
```

### Report (Reportes)
```sql
CREATE TABLE reports (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id),
  report_date DATE NOT NULL,
  total_minutes INT,
  productive_minutes INT,
  idle_minutes INT,
  efficiency_percentage DECIMAL(5,2),
  generated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, report_date)
);
```

## 5. Configuración de Entorno

### Variables de Entorno Backend
```
# Django
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=<generated-key>

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/timetracker

# JWT
JWT_SECRET=<generated-key>
JWT_EXPIRATION=3600
REFRESH_EXPIRATION=604800

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=app-password
```

### Variables de Entorno Frontend
```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_WS_URL=ws://localhost:8000
REACT_APP_ENV=development
```

## 6. Criterios de Aceptación MVP

- [ ] Usuarios pueden registrarse y loguearse
- [ ] Tracking básico funciona (START/STOP)
- [ ] Se capturan actividades automáticamente
- [ ] Reportes diarios generados correctamente
- [ ] Dashboard muestra datos en tiempo real
- [ ] Rate limiting implementado
- [ ] HTTPS configurado
- [ ] Tests > 80% cobertura backend
- [ ] Documentación API completa
- [ ] Performance < 500ms en APIs críticas

---

**Versión**: 1.0  
**Estado**: En Desarrollo  
**Última Actualización**: 21 de Mayo de 2026
