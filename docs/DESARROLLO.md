# Guía de Desarrollo

## Configuración del Entorno Local

### Requisitos Previos
- Python 3.10+
- Node.js 16+
- PostgreSQL 13+
- Git

### Backend Setup

1. **Crear entorno virtual**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos**
```bash
cp .env.example .env
# Editar .env con tus credenciales
python manage.py migrate
python manage.py createsuperuser
```

4. **Ejecutar servidor**
```bash
python manage.py runserver
```

El servidor estará en: `http://localhost:8000`

### Frontend Setup

1. **Instalar dependencias**
```bash
cd frontend
npm install
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con la URL del API
```

3. **Ejecutar servidor de desarrollo**
```bash
npm start
```

La aplicación estará en: `http://localhost:3000`

## Estructura de Commits

Usar el formato Conventional Commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: feat, fix, docs, style, refactor, test, chore

**Ejemplos**:
- `feat(tracking): add pause functionality`
- `fix(auth): handle token expiration correctly`
- `docs(api): update endpoint documentation`

## Testing

### Backend
```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov

# Test específico
pytest apps/timetracking/tests/test_models.py
```

### Frontend
```bash
# Ejecutar tests
npm test

# Con cobertura
npm test -- --coverage
```

## Estándares de Código

### Backend (Python)
- PEP 8 style guide
- Usar `black` para formateo
- `flake8` para linting
- Type hints en funciones críticas

### Frontend (JavaScript/React)
- ESLint + Prettier
- Componentes funcionales con hooks
- PropTypes o TypeScript
- Naming: camelCase para variables, PascalCase para componentes

## Workflow de Desarrollo

1. Crear rama feature
```bash
git checkout -b feature/descripcion-breve
```

2. Realizar cambios
3. Hacer commit siguiendo Conventional Commits
4. Hacer push a rama
```bash
git push origin feature/descripcion-breve
```

5. Crear Pull Request
6. Code review
7. Merge a develop

## Docker (Desarrollo)

```bash
docker-compose up -d
```

Esto levantará:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- PostgreSQL: localhost:5432

## Debugging

### Backend
```python
import pdb
pdb.set_trace()  # Breakpoint
```

### Frontend
- Chrome DevTools (F12)
- React Developer Tools extension
- Redux DevTools para estado

## Recursos Útiles

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

Última actualización: 21 de Mayo de 2026
