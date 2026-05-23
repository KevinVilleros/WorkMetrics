#  Guía de Contribución

## Bienvenida

¡Gracias por tu interés en contribuir! Estos son los lineamientos para asegurar un desarrollo ordenado y de calidad.

## Cómo Contribuir

### 1. Fork y Clonar

```bash
# Fork el repositorio en GitHub
# Clonar tu fork
git clone https://github.com/your-username/Sec-0,1-bet.git
cd Sec-0,1-bet

# Añadir upstream
git remote add upstream https://github.com/original/Sec-0,1-bet.git
```

### 2. Crear Rama Feature

```bash
git checkout develop
git pull upstream develop
git checkout -b feature/breve-descripcion
```

**Nomenclatura de ramas**:
- `feature/descripcion` - Nueva funcionalidad
- `fix/descripcion` - Corrección de bug
- `docs/descripcion` - Documentación
- `refactor/descripcion` - Refactorización

### 3. Realizar Cambios

- Sigue los estándares de código (ver abajo)
- Escribe tests para tu código
- Asegúrate de que todos los tests pasen
- Documenta cambios significativos

### 4. Commits

Usar Conventional Commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Tipos**:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Cambios de formato (sin lógica)
- `refactor`: Cambio de código sin nuevas features
- `test`: Agregar o actualizar tests
- `chore`: Cambios de build, dependencias, etc.

**Ejemplos**:
```
feat(tracking): add pause/resume functionality

Permite pausar y reanudar el tracking de tiempo durante una jornada.
Implementa validaciones para evitar pausas innecesarias.

Closes #123
```

```
fix(auth): handle expired tokens gracefully

Actualiza el middleware para manejar tokens expirados y refrescarlos automáticamente.

Fixes #456
```

### 5. Push y Pull Request

```bash
git push origin feature/descripcion
```

**En GitHub**: Crear Pull Request con descripción clara

**Template PR**:
```markdown
## Descripción
Breve descripción del cambio

## Tipo de Cambio
- [ ] Bug fix
- [ ] Nueva funcionalidad
- [ ] Breaking change
- [ ] Documentación

## Cómo fue testeado?
Describe los tests realizados

## Checklist
- [ ] Mi código sigue los estándares de código
- [ ] He ejecutado tests locales exitosamente
- [ ] He actualizado la documentación
- [ ] He agregado tests para la nueva funcionalidad
- [ ] No hay cambios innecesarios
```

### 6. Review y Merge

- Esperar revisión de código
- Atender comentarios/sugerencias
- Una vez aprobado, mergeará el maintainer

## Estándares de Código

### Python (Backend)

```python
# PEP 8 Style Guide

# Imports organizados
import os
from typing import Dict, List
from django.db import models

# Docstrings en clases y funciones
def calculate_efficiency(productive_minutes: int, total_minutes: int) -> float:
    """
    Calcula el porcentaje de eficiencia.
    
    Args:
        productive_minutes: Minutos productivos
        total_minutes: Total de minutos trabajados
        
    Returns:
        float: Porcentaje de eficiencia (0-100)
    """
    if total_minutes == 0:
        return 0.0
    return (productive_minutes / total_minutes) * 100
```

**Herramientas**:
```bash
# Formatear código
black backend/

# Linting
flake8 backend/

# Type checking
mypy backend/

# Todos juntos
pre-commit run --all-files
```

### JavaScript/React (Frontend)

```javascript
// ESLint + Prettier

// Nombrado claro
const calculateEfficiency = (productive, total) => {
  if (total === 0) return 0;
  return (productive / total) * 100;
};

// Componentes funcionales con hooks
const TimeTracker = ({ projectId }) => {
  const [isRunning, setIsRunning] = useState(false);
  
  return (
    <div className="tracker">
      {/* JSX */}
    </div>
  );
};

// PropTypes
TimeTracker.propTypes = {
  projectId: PropTypes.number.isRequired,
};
```

**Herramientas**:
```bash
npm run lint
npm run format
npm test
```

## Testing

### Backend

```bash
# Tests unitarios
pytest

# Con cobertura
pytest --cov=apps --cov-report=html

# Test específico
pytest apps/timetracking/tests/test_models.py::TestTimeEntry
```

**Ejemplo**:
```python
class TestCalculateEfficiency(TestCase):
    def test_normal_calculation(self):
        efficiency = calculate_efficiency(800, 1000)
        self.assertEqual(efficiency, 80.0)
    
    def test_zero_total_minutes(self):
        efficiency = calculate_efficiency(100, 0)
        self.assertEqual(efficiency, 0.0)
```

### Frontend

```bash
npm test
npm test -- --coverage
```

**Requisito**: Mínimo 80% de cobertura de código

## Reporting de Issues

### Formato de Bug Report

```markdown
**Descripción**
Describir brevemente el problema

**Pasos para Reproducir**
1. Ir a ...
2. Hacer click en ...
3. Ver error ...

**Comportamiento Esperado**
Debería mostrar ...

**Comportamiento Actual**
Muestra ...

**Environment**
- OS: [e.g., Ubuntu 20.04]
- Browser: [e.g., Chrome 95]
- Versión: [e.g., 1.0.0]

**Logs/Screenshots**
[Agregar si es relevante]
```

## Proceso de Release

1. Feature completa y testeada
2. PR revisado y aprobado
3. Merge a `develop`
4. Merge a `main` para release
5. Tag de versión (semver)
6. Notas de release

## Reconocimiento

Todos los contribuyentes serán reconocidos en:
- Archivo CONTRIBUTORS.md
- Página de créditos del proyecto
- Releases notes

## Preguntas?

- Abrir una issue con etiqueta `question`
- Contactar a los maintainers

---

¡Gracias por contribuir! 

**Última Actualización**: 21 de Mayo de 2026
