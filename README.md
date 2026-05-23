#  Sistema de Monitoreo de Eficiencia Laboral

## Descripción General

Sistema profesional para medir, monitorear y analizar las horas laborales de empleados, permitiendo evaluar su eficiencia, tiempo productivo/improductivo y otros factores críticos que impactan el desempeño organizacional.

##  Objetivos Principales

-  Tracking de tiempo en tiempo real
-  Registro automático de actividades
-  Análisis de eficiencia laboral
-  Identificación de tiempo perdido
-  Generación de reportes detallados
-  Dashboard de gestión ejecutiva

## ️ Estructura del Proyecto

```
├── backend/                 # API REST (Django)
├── frontend/                # Cliente Web (React)
├── docs/                    # Documentación
├── .config/                 # Configuraciones
├── README.md                # Este archivo
├── ARQUITECTURA.md          # Diseño del sistema
├── ESPECIFICACIONES.md      # Requisitos técnicos
├── .gitignore               # Git configuration
└── docker-compose.yml       # Orquestación de servicios
```

## ️ Stack Tecnológico

### Backend
- **Framework**: Django 4.x + Django REST Framework
- **Base de Datos**: PostgreSQL 13+
- **Autenticación**: JWT (JSON Web Tokens)
- **Servidor**: Gunicorn + Nginx

### Frontend
- **Biblioteca**: React 18+
- **Gestión de Estado**: Redux Toolkit
- **Estilos**: Tailwind CSS
- **Gráficos**: Chart.js / Recharts
- **HTTP**: Axios

### DevOps
- **Contenedorización**: Docker
- **Orquestación**: Docker Compose
- **Control de Versiones**: Git/GitHub

##  Requerimientos Previos

- Python 3.10+
- Node.js 16+ y npm
- PostgreSQL 13+
- Docker y Docker Compose
- Git

##  Inicio Rápido

### 1. Clonar Repositorio
```bash
git clone <repository-url>
cd Sec-0,1-bet
```

### 2. Configurar Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. Configurar Frontend
```bash
cd frontend
npm install
npm start
```

### 4. Con Docker (Recomendado)
```bash
docker-compose up -d
```

##  Documentación

- [Arquitectura del Sistema](./ARQUITECTURA.md)
- [Especificaciones Técnicas](./ESPECIFICACIONES.md)
- [Guía de Desarrollo](./docs/DESARROLLO.md)
- [API Documentation](./docs/API.md)

##  Seguridad

- Autenticación con JWT
- Encriptación de contraseñas con bcrypt
- HTTPS en producción
- Rate limiting implementado
- Validación de entrada en todos los endpoints

##  Métricas Clave

- **Horas Productivas**: Tiempo activamente trabajando
- **Tiempo Inactivo**: Períodos sin actividad registrada
- **Índice de Eficiencia**: % de productividad vs. horas totales
- **Análisis de Pausas**: Duración y frecuencia de descansos
- **Tiempo por Proyecto**: Distribución de horas por tarea

##  Roles de Usuario

- **Admin**: Acceso total al sistema
- **Gerente**: Visualizar reportes, gestionar empleados
- **Empleado**: Trackear tiempo, ver su propio desempeño

##  Roadmap

- [ ] v1.0: MVP con tracking básico
- [ ] v1.1: Reportes avanzados
- [ ] v1.2: Mobile app nativa
- [ ] v2.0: Analítica avanzada
- [ ] v2.1: Integraciones con herramientas externas

##  Contribución

Ver [CONTRIBUTING.md](./docs/CONTRIBUTING.md) para detalles.

##  Licencia

Proyecto propietario - Derechos reservados

##  Contacto

Para preguntas o sugerencias, contactar al equipo de desarrollo.

---

**Última actualización**: 21 de Mayo de 2026
# Sec-0-1-bet
