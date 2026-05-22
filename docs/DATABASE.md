# Configuración de Base de Datos

## PostgreSQL Setup

### Instalación

**Linux (Ubuntu/Debian)**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**macOS**
```bash
brew install postgresql
brew services start postgresql
```

**Windows**
Descargar desde: https://www.postgresql.org/download/windows/

### Crear Database y Usuario

```bash
# Conectar a PostgreSQL
sudo -u postgres psql

# Crear usuario
CREATE USER timetracker_user WITH PASSWORD 'secure_password_here';

# Crear base de datos
CREATE DATABASE timetracker_db OWNER timetracker_user;

# Permisos
ALTER ROLE timetracker_user SET client_encoding TO 'utf8';
ALTER ROLE timetracker_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE timetracker_user SET default_transaction_deferrable TO on;
ALTER ROLE timetracker_user SET timezone TO 'UTC';

# Verificar
\l
\du

# Salir
\q
```

### Connection String

```
postgresql://timetracker_user:secure_password_here@localhost:5432/timetracker_db
```

## Migraciones Django

```bash
# Crear migraciones
python manage.py makemigrations

# Ver SQL de migraciones
python manage.py sqlmigrate app_name migration_number

# Aplicar migraciones
python manage.py migrate

# Ver estado de migraciones
python manage.py showmigrations
```

## Backup y Restore

### Backup
```bash
pg_dump -U timetracker_user -d timetracker_db > backup.sql

# Con compresión
pg_dump -U timetracker_user -d timetracker_db | gzip > backup.sql.gz
```

### Restore
```bash
psql -U timetracker_user -d timetracker_db < backup.sql

# Desde comprimido
gunzip -c backup.sql.gz | psql -U timetracker_user -d timetracker_db
```

## Índices para Optimización

```sql
-- Índices en time_entries
CREATE INDEX idx_user_date ON time_entries(user_id, start_time DESC);
CREATE INDEX idx_project_date ON time_entries(project_id, start_time DESC);
CREATE INDEX idx_status ON time_entries(status);

-- Índices en activities
CREATE INDEX idx_entry_time ON activities(time_entry_id, captured_at);
CREATE INDEX idx_user_app ON activities(user_id, application);

-- Índices en reports
CREATE INDEX idx_report_user_date ON reports(user_id, report_date DESC);
CREATE INDEX idx_efficiency ON reports(efficiency_percentage DESC);

-- Índices en users
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_role ON users(role);
```

## Consultas Útiles

### Top usuarios por eficiencia
```sql
SELECT 
  u.id,
  u.first_name,
  u.last_name,
  AVG(r.efficiency_percentage) as avg_efficiency,
  COUNT(r.id) as days_tracked
FROM users u
LEFT JOIN reports r ON u.id = r.user_id
WHERE r.report_date >= DATE_TRUNC('month', NOW())
GROUP BY u.id
ORDER BY avg_efficiency DESC;
```

### Horas totales por proyecto
```sql
SELECT 
  p.name,
  SUM(te.duration_minutes) as total_minutes,
  COUNT(DISTINCT te.user_id) as users
FROM projects p
LEFT JOIN time_entries te ON p.id = te.project_id
WHERE DATE(te.start_time) >= DATE_TRUNC('month', NOW())
GROUP BY p.id, p.name
ORDER BY total_minutes DESC;
```

---

**Última Actualización**: 21 de Mayo de 2026
