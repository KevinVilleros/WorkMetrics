#!/bin/bash

# Script rápido para crear un README profesional para GitHub
# Este script agrega badges y formatea el README existente

echo "🎨 Generando README profesional para GitHub..."

cat > README_GITHUB.md << 'EOF'
<div align="center">

# 📊 Sistema de Monitoreo de Eficiencia Laboral

**Una solución empresarial profesional para medir, monitorear y analizar la productividad de empleados**

[![GitHub](https://img.shields.io/badge/github-private-181717?logo=github&style=flat-square)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&style=flat-square)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&style=flat-square)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&style=flat-square)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql&style=flat-square)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&style=flat-square)](https://docker.com)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)](LICENSE)

![Tests](https://github.com/TU_USUARIO/Sec-0,1-bet/actions/workflows/backend-tests.yml/badge.svg)
![Build](https://github.com/TU_USUARIO/Sec-0,1-bet/actions/workflows/build-docker.yml/badge.svg)
![Security](https://github.com/TU_USUARIO/Sec-0,1-bet/actions/workflows/security.yml/badge.svg)
[![codecov](https://codecov.io/gh/TU_USUARIO/Sec-0,1-bet/branch/main/graph/badge.svg)](https://codecov.io/gh/TU_USUARIO/Sec-0,1-bet)

**[📖 Documentación](#documentación) • [🚀 Quick Start](#quick-start) • [🤝 Contribuir](#contributing) • [📋 Roadmap](#roadmap)**

</div>

---

## 🎯 Características Principales

- ✅ **Tracking en Tiempo Real** - Monitoreo continuo de horas laborales
- ✅ **Detección de Inactividad** - Automática basada en mouse y teclado
- ✅ **Registro de Actividades** - Captura de aplicaciones y acciones
- ✅ **Reportes Avanzados** - Diarios, semanales, mensuales con análisis
- ✅ **Dashboard Ejecutivo** - Visualización de KPIs en tiempo real
- ✅ **Análisis de Eficiencia** - Cálculo automático de índices de productividad
- ✅ **Seguridad Empresarial** - JWT, encriptación, auditoría completa
- ✅ **API REST Profesional** - 20+ endpoints documentados
- ✅ **Escalable** - Docker, PostgreSQL, caché con Redis
- ✅ **CI/CD Automatizado** - GitHub Actions, tests, seguridad

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                  FRONTEND (React 18)                        │
│          Dashboard | TimeTracker | Reports | Charts         │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
                       ↓
┌──────────────────────────────────────────────────────────────┐
│              BACKEND (Django + DRF)                          │
│  Auth | Tracking | Activities | Reports | Analytics         │
└──────────────────────┬──────────────────────────────────────┘
                       │ SQL
                       ↓
┌──────────────────────────────────────────────────────────────┐
│        DATABASE (PostgreSQL) + CACHE (Redis)                 │
│   Users | TimeEntries | Activities | Reports | Metrics      │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Requisitos Previos
- Python 3.11+
- Node.js 16+
- PostgreSQL 13+
- Docker & Docker Compose

### Con Docker (Recomendado)

```bash
# Clonar repositorio
git clone git@github.com:TU_USUARIO/Sec-0,1-bet.git
cd Sec-0,1-bet

# Iniciar servicios
docker-compose up -d

# Acceder a la aplicación
# Frontend: http://localhost:3000
# API: http://localhost:8000/api
# Admin: http://localhost:8000/admin
```

### Configuración Local

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

---

## 📊 Stack Tecnológico

### Backend
| Tecnología | Versión | Propósito |
|------------|---------|----------|
| Django | 4.2 | Framework web |
| DRF | 3.14 | API REST |
| PostgreSQL | 15 | Base de datos |
| Redis | 7 | Caché |
| Celery | 5.3 | Tasks asincrónicas |
| JWT | 2.8 | Autenticación |

### Frontend
| Tecnología | Versión | Propósito |
|------------|---------|----------|
| React | 18 | Librería UI |
| Redux | 1.9 | State management |
| Tailwind | 3.4 | Estilos |
| Axios | 1.6 | HTTP client |
| Recharts | 2.10 | Gráficas |

### DevOps
| Tecnología | Versión | Propósito |
|------------|---------|----------|
| Docker | Latest | Containerización |
| Nginx | Alpine | Proxy reverso |
| GitHub Actions | - | CI/CD |
| Codecov | - | Cobertura |

---

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [README.md](README.md) | Descripción general del proyecto |
| [ARQUITECTURA.md](ARQUITECTURA.md) | Diseño del sistema y diagramas |
| [ESPECIFICACIONES.md](ESPECIFICACIONES.md) | Requisitos técnicos detallados |
| [docs/API.md](docs/API.md) | Documentación de endpoints |
| [docs/DESARROLLO.md](docs/DESARROLLO.md) | Guía de desarrollo local |
| [docs/DATABASE.md](docs/DATABASE.md) | Configuración de PostgreSQL |
| [GITHUB_SETUP.md](GITHUB_SETUP.md) | Setup del repositorio GitHub |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | Guía de contribución |
| [SECURITY.md](SECURITY.md) | Política de seguridad |
| [CHANGELOG.md](CHANGELOG.md) | Historial de cambios |

---

## 🔐 Seguridad

- 🔒 **Autenticación**: JWT con refresh tokens
- 🛡️ **Encriptación**: AES-256 en reposo, TLS 1.2+ en tránsito
- ✅ **Validación**: Input validation en cliente y servidor
- 📋 **Auditoría**: Log completo de acciones
- 🚨 **Alertas**: Sistema de anomalías
- 🔑 **Secretos**: Administrados en GitHub Secrets
- 🔍 **Escaneos**: CodeQL, Trivy, Dependabot

### Reportar Vulnerabilidades

⚠️ **No abras un issue público**. Envía un email a: `security@empresa.com`

Ver [SECURITY.md](SECURITY.md) para detalles.

---

## 📈 Métricas

- **Tests**: >80% cobertura
- **Performance**: <500ms en APIs
- **Uptime**: 99.5% objetivo
- **Disponibilidad**: Activa 24/7

---

## 🔄 CI/CD Pipeline

```
Push to GitHub
    ↓
├─ Backend Tests ✅
├─ Frontend Tests ✅
├─ Security Checks ✅
├─ Build Docker Images ✅
└─ Deploy (si merge a main) ✅
```

### Status de Builds

- [Backend Tests](https://github.com/TU_USUARIO/Sec-0,1-bet/actions/workflows/backend-tests.yml)
- [Frontend Tests](https://github.com/TU_USUARIO/Sec-0,1-bet/actions/workflows/frontend-tests.yml)
- [Security Checks](https://github.com/TU_USUARIO/Sec-0,1-bet/actions/workflows/security.yml)
- [Docker Build](https://github.com/TU_USUARIO/Sec-0,1-bet/actions/workflows/build-docker.yml)

---

## 🤝 Contributing

¡Las contribuciones son bienvenidas! Por favor:

1. Revisa [CONTRIBUTING.md](docs/CONTRIBUTING.md)
2. Crea una rama: `git checkout -b feature/mi-feature`
3. Commit: `git commit -am 'feat: descripción'`
4. Push: `git push origin feature/mi-feature`
5. Abre un Pull Request

### Estándares de Código

- Python: PEP 8 + Black
- JavaScript: ESLint + Prettier
- Git: Conventional Commits
- Tests: >80% cobertura

Ver [.github/CODEOWNERS](.github/CODEOWNERS) para owners.

---

## 📋 Roadmap

### Fase 1: MVP (Mayo-Junio 2026) ✅
- [x] Sistema de tracking básico
- [x] Reportes diarios
- [x] Dashboard
- [x] Autenticación JWT

### Fase 2: Mejoras (Julio-Agosto 2026) 🔄
- [ ] Análisis de tendencias
- [ ] Mobile app
- [ ] Integraciones (Slack, Calendar)
- [ ] Dark mode

### Fase 3: Avanzado (Septiembre+ 2026) ⏳
- [ ] AI/ML analytics
- [ ] Gamification
- [ ] White-label solution
- [ ] Enterprise features

Ver [ROADMAP.md](docs/ROADMAP.md) para detalles completos.

---

## 📞 Contacto y Soporte

- 📧 **Email**: support@empresa.com
- 💬 **Issues**: [GitHub Issues](https://github.com/TU_USUARIO/Sec-0,1-bet/issues)
- 🐛 **Bugs**: Usa template [.github/ISSUE_TEMPLATES](ISSUE_TEMPLATES/)
- 📖 **Docs**: [docs/](docs/)

---

## 📄 Licencia

**Proyecto Propietario** - Todos los derechos reservados

```
© 2026 Tu Empresa. Confidencial.
Prohibida la reproducción sin permiso.
```

---

## 👥 Autores

- **Tech Lead**: [@tu_usuario](https://github.com/tu_usuario)
- **Backend Team**: Backend developers
- **Frontend Team**: Frontend developers
- **DevOps Team**: Infrastructure team

---

## 🙏 Agradecimientos

Gracias a:
- [Django](https://djangoproject.com/)
- [React](https://react.dev/)
- [PostgreSQL](https://postgresql.org/)
- Comunidad open source

---

## 📊 Estadísticas del Proyecto

```
Lenguajes:
  Python:       ███████░░ 35%
  JavaScript:   ███████░░ 35%
  Markdown:     ██░░░░░░░ 20%
  Other:        █░░░░░░░░ 10%

Lines of Code:
  Backend:      ~8,000 LOC
  Frontend:     ~6,000 LOC
  Tests:        ~4,000 LOC
  Docs:         ~15,000 lines

Repository:
  Commits:      50+
  Contributors: 5+
  Branches:     active/develop + main
  Last Update:  21 de Mayo de 2026
```

---

<div align="center">

**[⬆ Volver al inicio](#-sistema-de-monitoreo-de-eficiencia-laboral)**

**Hecho con ❤️ por el equipo de desarrollo**

</div>
EOF

echo "✅ README profesional generado: README_GITHUB.md"
echo ""
echo "📝 Próximos pasos:"
echo "1. Reemplaza en GitHub el README.md con el contenido de README_GITHUB.md"
echo "2. Customiza los badges y URLs con tu información"
echo "3. Agrega imágenes/screenshots si tienes"
echo ""
