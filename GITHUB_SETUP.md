#  Guía: Configurar Repositorio Privado en GitHub

## Paso 1: Inicializar Git Local

```bash
cd /home/kin/Escritorio/Sec-0,1-bet

# Inicializar repositorio
git init

# Configurar usuario git (si no lo has hecho)
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@example.com"

# Agregar todos los archivos
git add .

# Commit inicial
git commit -m "chore: proyecto inicial - estructura profesional completa

- Iniciado sistema de monitoreo de eficiencia laboral
- Stack: Django + React + PostgreSQL
- Documentación completa
- GitHub Actions CI/CD
- Docker setup
- Tests framework
- Seguridad implementada"
```

## Paso 2: Crear Repositorio en GitHub (Privado)

1. Ir a [github.com/new](https://github.com/new)

2. Llenar los detalles:
   - **Repository name**: `Sec-0,1-bet` (o el nombre que prefieras)
   - **Description**: "Sistema profesional de monitoreo de eficiencia laboral"
   - **Visibility**:  **Private** (IMPORTANTE)
   - **Initialize this repository**: NO (dejar sin marcar)
   - Click **Create repository**

## Paso 3: Conectar Repositorio Local con GitHub

```bash
# Agregar el repositorio remoto
git remote add origin https://github.com/TU_USUARIO/Sec-0,1-bet.git

# Renombrar rama principal (si necesario)
git branch -M main

# Hacer push del código
git push -u origin main

# Verificar conexión
git remote -v
```

## Paso 4: Configurar Ramas Protegidas

En GitHub, ve a **Settings → Branches → Add rule**

### Rama: `main`

```
- Require a pull request before merging: 
- Require status checks to pass before merging: 
  - Require branches to be up to date before merging: 
  - Require status checks to pass: 
    - Backend Tests
    - Frontend Tests
    - Security Checks
- Dismiss stale pull request approvals: 
- Require code reviews before merging: 
  - Require review from Code Owners: 
  - Require 2 pull request reviews: 
  - Require reviews from pull request authors: 
- Require up-to-date branches: 
- Require conversation resolution before merging: 
- Require deployments to succeed: ⬜ (opcional)
```

### Rama: `develop`

```
- Require a pull request before merging: 
- Require status checks to pass before merging: 
- Dismiss stale pull request approvals: 
- Require code reviews before merging: 
  - Require 1 pull request review: 
```

## Paso 5: Configurar Secretos (GitHub Actions)

Ve a **Settings → Secrets and variables → Actions → New repository secret**

Agrega estos secretos:

### Para CI/CD:
```
REGISTRY_USERNAME=tu_usuario
REGISTRY_PASSWORD=tu_token_github
```

### Para Deploys (opcional):
```
DEPLOY_SERVER_HOST=tu.servidor.com
DEPLOY_SERVER_USER=deploy_user
DEPLOY_SERVER_KEY=private_ssh_key_base64
DEPLOY_WEBHOOK_SECRET=webhook_secret
```

## Paso 6: Configurar Colaboradores

**Settings → Access → Collaborators and teams → Add people**

Agrega a tus colaboradores:
-  Admin: Acceso total
-  Maintain: Gestionar sin eliminar repo
-  Write: Hacer push y PR
-  Triage: Crear issues y PR
-  Read: Solo lectura

## Paso 7: Configurar Project Board (Opcional)

**Projects → New**

```
- Project name: Sec-0,1-bet Development
- Template: Table (o Kanban)
- Automation: Enabled
```

Columnas propuestas:
```
-  Backlog
-  Sprint Planning
- ⏳ In Progress
-  Code Review
-  Done
-  Bugs
```

## Paso 8: Configurar Ruleset (Opcional - GitHub Pro+)

**Settings → Rules → New ruleset**

```
- Name: Production Safety
- Enforcement: Active
- Target branches: main
- Rules:
   Require pull request reviews (2)
   Dismiss stale approvals
   Require status checks
   Require branches to be up to date
   Block force pushes
   Block deletions
```

## Paso 9: Habilitar Features Avanzados

**Settings → Code security and analysis**

Habilitar:
-  Dependabot alerts
-  Dependabot security updates
-  Dependabot version updates (ya configurado)
-  Private vulnerability reporting
-  Code scanning (si tienes Advanced Security)
-  Secret scanning
-  Push protection

## Paso 10: Crear Rama de Desarrollo

```bash
git checkout -b develop
git push -u origin develop
```

## Paso 11: Crear CODEOWNERS File

Crea un archivo `.github/CODEOWNERS`:

```
# Global
* @tu_usuario

# Backend
backend/ @tu_usuario @otro_backend_dev
apps/users/ @especialista_auth
apps/reports/ @especialista_reports

# Frontend
frontend/ @tu_usuario @otro_frontend_dev
src/components/ @especialista_ui

# DevOps
docker-compose.yml @devops_engineer
.github/workflows/ @devops_engineer
.config/ @devops_engineer

# Docs
docs/ @tech_lead
README.md @tech_lead
```

## Paso 12: Proteger Secretos

**Settings → Security → Secret scanning**

-  Push protection for custom patterns
- Agregar patrones para detectar:
  - Private keys
  - API keys
  - Database credentials

## Paso 13: Habilitar Autolinks (Opcional)

**Settings → Autolinks**

```
Reference prefix: #
Target URL: https://github.com/TU_USUARIO/Sec-0,1-bet/issues/<num>
```

## Paso 14: Configurar Webhooks (Opcional)

**Settings → Webhooks**

Para integración con Slack/Discord:

```
Payload URL: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
Content type: application/json
Events:
  - Pull requests
  - Issues
  - Push
  - Repository
```

---

##  Checklist Final

- [ ] Repositorio creado y privado
- [ ] Código hecho push a main
- [ ] Rama develop creada
- [ ] Ramas protegidas configuradas
- [ ] Secretos agregados
- [ ] CODEOWNERS file creado
- [ ] GitHub Actions ejecutándose
- [ ] Dependabot activado
- [ ] Secret scanning activado
- [ ] Colaboradores agregados
- [ ] README.md actualizado
- [ ] CONTRIBUTING.md revisado

---

##  Seguridad: Lista de Verificación

- [ ] Repositorio: PRIVATE 
- [ ] No incluir .env en git 
- [ ] .gitignore completo 
- [ ] Ramas protegidas 
- [ ] 2 reviewers requeridos 
- [ ] Status checks requeridos 
- [ ] SECURITY.md presente 
- [ ] CODE_OF_CONDUCT.md presente 
- [ ] Secret scanning activo 
- [ ] Dependabot updates activo 

---

##  Comandos Útiles de Git

```bash
# Ver estado
git status

# Ver commits
git log --oneline -10

# Crear rama feature
git checkout -b feature/descripcion
git push -u origin feature/descripcion

# Hacer PR localmente
git fetch origin
git checkout origin/main
git checkout -b pr-branch

# Sincronizar con main
git fetch origin
git rebase origin/main

# Eliminar rama local
git branch -d feature/descripcion

# Eliminar rama remota
git push origin --delete feature/descripcion
```

---

## 🆘 Solución de Problemas

### Error: "Permission denied (publickey)"
```bash
# Generar SSH key
ssh-keygen -t ed25519 -C "tu.email@gmail.com"

# Agregar a SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copiar y agregar a GitHub: Settings → SSH Keys
cat ~/.ssh/id_ed25519.pub
```

### Error: "Repository not found"
- Verifica que el repositorio sea privado y tengas acceso
- Verifica que hayas hecho login con `git config`

### Error: "branch is protected"
- Necesitas PR para mergear a main/develop
- Necesitas 2 reviews (o lo que configuraste)
- Necesitas pasar todos los tests

---

**Configuración Completada**: 21 de Mayo de 2026

¡Tu repositorio GitHub profesional y privado está listo! 
