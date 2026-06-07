# MetricLab - Sistema de Monitoreo de Eficiencia Laboral

## 📊 INFORME DEL PROGRAMA

### ¿Qué es MetricLab?

MetricLab es una **plataforma profesional de monitoreo de eficiencia laboral** que permite a empresas rastrear, analizar y reportar sobre el desempeño, tiempo productivo y actividades de empleados en tiempo real.

---

## 🎯 Funcionalidades Principales

### 1. **Tracking de Tiempo en Tiempo Real**
- Registro automático de inicio/cierre de sesión
- Detección de inactividad del usuario
- Medición de horas productivas vs. horas inactivas
- Cálculo automático de índices de eficiencia

### 2. **Detección de Actividades**
- **Detección de personas con cámara**: Utiliza MediaPipe Face Detection
- Monitoreo de presencia del empleado en pantalla
- Análisis de patrones de actividad
- Registro de pausas y descansos automáticos

### 3. **Generación de Reportes**
- **Reportes diarios, semanales y mensuales** de productividad
- Exportación en múltiples formatos
- Análisis de tendencias de uso laboral
- Identificación de tiempo perdido y oportunidades de mejora

### 4. **Dashboard Ejecutivo**
- Visualización en tiempo real de métricas
- Gráficos y estadísticas por empleado/departamento
- KPIs de eficiencia
- Alertas de baja productividad

### 5. **Gestión de Usuarios y Roles**
- **3 niveles de acceso**:
  - **Administrador**: Control total del sistema, gestión de usuarios
  - **Gerente**: Visualización de reportes, supervisión de equipos
  - **Empleado**: Trackeo personal, visualización de su desempeño
- Autenticación segura con JWT (JSON Web Tokens)

---

## 🏗️ Arquitectura Técnica

### **Backend (API REST - Django)**
- Framework: Django 4.x + Django REST Framework
- Base de Datos: PostgreSQL / SQLite (para desarrollo)
- Autenticación: JWT
- Servidor: Gunicorn + Nginx (producción)

**Módulos principales:**
- `users/` - Gestión de usuarios y autenticación
- `timetracking/` - Registro de horas y sesiones
- `activities/` - Detección y registro de actividades
- `reports/` - Generación de reportes
- `analytics/` - Análisis de datos y métricas

### **Frontend (Interfaz Web - React)**
- Biblioteca: React 18+
- Gestión de Estado: Redux Toolkit
- Estilos: Tailwind CSS
- Visualización: Chart.js / Recharts
- HTTP: Axios

**Componentes principales:**
- Dashboard de métricas
- Visor de cámara en tiempo real
- Generador de reportes
- Gestión de usuarios
- Gráficos interactivos

### **Desktop (Electron)**
- Wrapper Electron para ejecutable de Windows
- Permite usar MetricLab como aplicación desktop
- Acceso a cámara del dispositivo
- Generador: `electron-packager` → `MetricLab.exe`

---

## 📈 Métricas que Calcula

1. **Horas Productivas**: Tiempo activamente trabajando
2. **Tiempo Inactivo**: Períodos sin movimiento del usuario
3. **Índice de Eficiencia**: `(Horas Productivas / Horas Totales) × 100%`
4. **Análisis de Pausas**: Duración y frecuencia de descansos
5. **Tiempo por Proyecto/Tarea**: Distribución de horas
6. **Tendencias**: Análisis diario/semanal/mensual

---

## 🚀 Métodos de Ejecución

### **Opción 1: Usar el Launcher Python (RECOMENDADO)**
```batch
MetricLab.bat
```
- Automático: venv, dependencias, migraciones, servidores
- Ideal para desarrollo y pruebas
- No empaqueta, es más ligero
- Tamaño: ~5-10 MB (solo archivos del proyecto)

### **Opción 2: Ejecutable de Escritorio (Electron + Windows)**
```batch
cd frontend
npm run electron:package
```
- Crea: `frontend/dist/MetricLab-win32-x64/MetricLab.exe`
- Interfaz de usuario en Electron
- Acceso a cámara del dispositivo
- Tamaño: ~200-250 MB (incluye Electron runtime)

### **Opción 3: Con Docker**
```batch
docker-compose up -d
```
- Ambiente completamente aislado
- Recomendado para producción
- No requiere instalar dependencias locales

### **Opción 4: Standalone PyInstaller**
```batch
pyinstaller metriclab.spec
```
- Crea: `dist/MetricLab.exe`
- Incluye Python + todas las dependencias
- Tamaño: ~100-150 MB

---

## 🎬 Características de Detección de Cámara

La aplicación incluye un componente **PersonDetector** que:

1. **Accede a la cámara del dispositivo** (con permiso del usuario)
2. **Detecta presencia de personas** usando MediaPipe Face Detection
3. **Rastrea patrones de actividad**:
   - Presencia en pantalla
   - Movimiento del rostro/cabeza
   - Nivel de atención estimado
4. **Genera eventos de atención**:
   - Inicio de sesión
   - Cambios de estado (activo/inactivo)
   - Fin de sesión
5. **Calcula FPS (fotogramas por segundo)** para monitoreo de rendimiento

---

## 💾 Base de Datos - Tablas Principales

| Tabla | Descripción |
|-------|-----------|
| `users` | Usuarios del sistema con roles |
| `time_tracking` | Registros de sesiones de trabajo |
| `activities` | Eventos de actividad detectados |
| `reports` | Reportes generados |
| `analytics_snapshots` | Datos agregados para análisis |

---

## 🔒 Seguridad Implementada

- ✓ Autenticación JWT (tokens seguros)
- ✓ Encriptación de contraseñas con bcrypt
- ✓ HTTPS en producción
- ✓ Rate limiting (límite de requests)
- ✓ Validación de entrada en todos endpoints
- ✓ Control de acceso basado en roles (RBAC)

---

## 📊 Puertos de Servicio

| Servicio | Puerto | URL |
|----------|--------|-----|
| Backend API | 8000 | http://localhost:8000/api |
| Frontend Web | 3000 | http://localhost:3000 |
| PostgreSQL | 5432 | Internal |

---

## 🔧 Requisitos Previos

- Python 3.10+
- Node.js 16+ (para frontend)
- PostgreSQL 13+ (o SQLite para dev)
- Git
- Docker (opcional, para containerización)

---

## 📋 Flujo de Uso Típico

### **Para Empleados:**
1. Iniciar sesión en MetricLab
2. Hacer clic en "Iniciar Cámara" para comenzar monitoreo
3. El sistema rastrea automáticamente su actividad
4. Al finalizar jornada, hacer clic en "Finalizar Sesión"
5. Sistema calcula automáticamente métricas y las envía al backend

### **Para Gerentes:**
1. Acceder al Dashboard
2. Ver métricas en tiempo real del equipo
3. Generar reportes semanales/mensuales
4. Identificar empleados con baja productividad
5. Tomar decisiones basadas en datos

### **Para Administradores:**
1. Gestionar usuarios del sistema
2. Asignar roles y permisos
3. Configurar parámetros de tracking
4. Monitorear salud del sistema
5. Exportar datos para auditoría

---

## 📦 Estructura de Carpetas del Proyecto

```
MetricLab/
├── backend/                    # API REST (Django)
│   ├── apps/
│   │   ├── users/              # Gestión de usuarios
│   │   ├── timetracking/       # Tracking de tiempo
│   │   ├── activities/         # Registro de actividades
│   │   ├── reports/            # Generación de reportes
│   │   └── analytics/          # Análisis y métricas
│   ├── config/                 # Configuración de Django
│   └── utils/                  # Utilidades compartidas
│
├── frontend/                   # Interfaz React
│   ├── src/
│   │   ├── components/         # Componentes UI
│   │   │   ├── PersonDetector/ # Detección de cámara
│   │   │   ├── Dashboard/      # Panel principal
│   │   │   ├── TimeTracker/    # Tracker de tiempo
│   │   │   └── ReportView/     # Visor de reportes
│   │   ├── services/           # Servicios API
│   │   ├── redux/              # Gestión de estado
│   │   ├── pages/              # Páginas principales
│   │   └── utils/              # Utilidades frontend
│   ├── public/                 # Archivos estáticos
│   ├── electron.js             # Main process de Electron
│   └── package.json            # Dependencias npm
│
├── docs/                       # Documentación del proyecto
├── MetricLab.bat               # Launcher para Windows
├── metriclab_launcher.py       # Launcher en Python
├── docker-compose.yml          # Orquestación de servicios
└── README.md                   # Documentación principal
```

---

## ✅ Estado Actual del Proyecto

- ✓ Backend API completamente funcional
- ✓ Frontend React con componentes de tracking
- ✓ Detección de cámara integrada (MediaPipe)
- ✓ Sistema de reportes implementado
- ✓ **Ejecutable Electron para Windows (MetricLab.exe) generado**
- ✓ Autenticación y roles configurados
- ✓ Docker ready para producción

---

## 🎯 Objetivo Final

**Proporcionar a empresas una herramienta integral para:**
- Medir objetivamente la productividad de empleados
- Identificar patrones de inactividad
- Tomar decisiones basadas en datos
- Mejorar la gestión de recursos humanos
- Mantener privacidad y seguridad de datos

---

---

# Construir MetricLab.exe para Windows

## Opción 1: Usar el launcher Python directamente (SIN empaquetar)

```batch
MetricLab.bat
```

Este método es **recomendado** porque:
- ✓ No requiere PyInstaller
- ✓ Automáticamente detecta cambios en el código
- ✓ Más fácil de mantener
- ✓ Funciona en cualquier máquina con Python instalado

---

## Opción 2: Crear un ejecutable standalone (.exe con PyInstaller)

### Requisitos previos:
```batch
pip install pyinstaller
```

### Generar el ejecutable:
```batch
REM Desde la raíz del proyecto
pyinstaller --onefile --console ^
    --add-data "backend;backend" ^
    --add-data "frontend;frontend" ^
    --add-data "docs;docs" ^
    --name MetricLab ^
    metriclab_launcher.py
```

O simplemente:
```batch
pyinstaller metriclab.spec
```

### Resultado:
- Ejecutable: `dist/MetricLab.exe`
- Tamaño: ~100-150 MB (incluye Python + dependencias)
- Instalación: Copiar `dist/` a cualquier máquina con Windows

---

## Opción 3: Crear un instalador (.msi)

```batch
pip install msiexec
REM Crear instalador con WiX Toolset (requiere instalación adicional)
```

---

## Uso

### Método 1 (Recomendado):
```batch
MetricLab.bat
```

### Método 2 (Si compilaste con PyInstaller):
```batch
dist\MetricLab.exe
```

---

## Qué hace el launcher:

1. ✓ Verifica/crea entorno virtual
2. ✓ Instala dependencias Windows-específicas
3. ✓ Crea archivo `.env` para SQLite
4. ✓ Ejecuta migraciones de Django
5. ✓ Inicia servidor backend (puerto 8000)
6. ✓ Inicia servidor frontend (puerto 3000, si npm disponible)
7. ✓ Muestra estado de ambos servidores
8. ✓ No abre navegadores automáticamente

---

## Acceso a la aplicación:

Una vez iniciada, puedes acceder a:

- **Backend API**: http://localhost:8000/api
- **Frontend Web**: http://localhost:3000 (si npm está instalado)

---

## Solución de problemas:

### "Python no está en PATH"
```
Descarga Python desde https://www.python.org/downloads/
Marca la opción: "Add Python to PATH"
```

### "npm no encontrado"
```
Descarga Node.js desde https://nodejs.org
El backend seguirá funcionando sin npm
```

### "Puerto 8000 o 3000 ya en uso"
```
El launcher lo detectará y mostrará una advertencia
Los servidores intentarán iniciar de todas formas
```

### "Permiso denegado al ejecutar .bat"
```
Click derecho > Propiedades > Desbloquear
O ejecutar como administrador
```

---

## Compilar con PyInstaller (paso a paso):

```batch
REM 1. Instalar PyInstaller
pip install pyinstaller

REM 2. Navegar a la carpeta del proyecto
cd C:\ruta\a\MetricLab

REM 3. Crear el ejecutable (onefile = un único .exe)
pyinstaller --onefile ^
    --console ^
    --add-data "backend;backend" ^
    --add-data "frontend;frontend" ^
    --add-data "docs;docs" ^
    --name MetricLab ^
    metriclab_launcher.py

REM 4. El .exe estará en la carpeta 'dist'
REM   Puedes copiar dist\MetricLab.exe a cualquier lado
```

**Resultado final**: `dist/MetricLab.exe` (ejecutable standalone)
