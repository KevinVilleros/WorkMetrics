# MetricLab en Windows - Opciones de Ejecución

## 🚀 **OPCIÓN 1: MetricLab.bat (RECOMENDADA)**

**Archivo:** `MetricLab.bat`

```batch
MetricLab.bat
```

**Ventajas:**
- ✓ Ejecutable único y simple
- ✓ Todo automático: crea venv, instala dependencias, ejecuta migraciones
- ✓ Limpio: no abre navegadores
- ✓ Muestra estado claro de la aplicación
- ✓ Fácil de usar

**Qué hace:**
1. Verifica Python instalado
2. Ejecuta `metriclab_launcher.py`
3. Inicia backend (Django) en puerto 8000
4. Inicia frontend (React) en puerto 3000 si npm disponible
5. Muestra estado de ambos servidores

---

## 🐍 **OPCIÓN 2: Python directo**

```batch
python metriclab_launcher.py
```

**Ventajas:**
- ✓ Control total sobre el proceso
- ✓ Logs detallados
- ✓ Mismo comportamiento que MetricLab.bat

**Ventajas sobre el batch:**
- Mejor manejo de errores
- Output más legible
- Fácil de mantener

---

## 📦 **OPCIÓN 3: Ejecutable .exe (standalone)**

Requiere compilación con PyInstaller:

```batch
pip install pyinstaller
pyinstaller metriclab.spec
```

Luego ejecutar:
```batch
dist\MetricLab.exe
```

**Ventajas:**
- ✓ Funciona sin Python instalado
- ✓ Se puede distribuir como ejecutable
- ✓ ~150 MB

**Desventajas:**
- ✗ Más lento al iniciar
- ✗ Tamaño más grande

---

## 📋 **COMPARATIVA**

| Característica | MetricLab.bat | metriclab_launcher.py | MetricLab.exe |
|---|---|---|---|
| Tamaño | ~5 KB | ~15 KB | ~150 MB |
| Velocidad | Rápido | Rápido | Más lento |
| Requiere Python | ✓ Sí | ✓ Sí | ✗ No |
| Facilidad de uso | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Mantenimiento | Fácil | Fácil | Complejo |

**Recomendación:** Usa **MetricLab.bat** para desarrollo. Usa **MetricLab.exe** si necesitas distribuir.

---

## 🔧 **CONFIGURACIÓN**

El launcher automáticamente crea/valida:

- `backend/venv/` - Entorno virtual Python
- `backend/.env` - Variables de entorno (SQLite)
- `backend/db.sqlite3` - Base de datos (SQLite)
- `frontend/node_modules/` - Dependencias Node (si npm disponible)

---

## 📊 **ESTADO DE APLICACIÓN**

Al iniciar, verás algo como:

```
============================================================
        METRICLAB - ESTADO DE LA APLICACIÓN
============================================================

Backend (Django):
  Estado: ✓ Ejecutándose
  URL: http://localhost:8000
  API: http://localhost:8000/api

Frontend (React):
  Estado: ✓ Ejecutándose
  URL: http://localhost:3000

============================================================
Presiona Ctrl+C para detener la aplicación
============================================================
```

---

## ✅ **ACCESO A LA APLICACIÓN**

Una vez en ejecución:

**API Backend:**
- http://localhost:8000/api

**Frontend Web:**
- http://localhost:3000

**Admin Django (si creaste superuser):**
- http://localhost:8000/admin

---

## ⚠️ **REQUISITOS**

### Mínimo para ejecutar:
- **Windows 10/11** (64-bit)
- **Python 3.10+** con pip

### Para frontend (opcional):
- **Node.js 16+** con npm

### Verificar:
```batch
python --version
node --version
npm --version
```

---

## 🐛 **TROUBLESHOOTING**

### "Python no está instalado"
```
Descarga desde: https://www.python.org/downloads/
Marca: "Add Python to PATH"
Reinicia la terminal
```

### "npm no disponible"
```
Descarga Node.js desde: https://nodejs.org
El backend funcionará sin npm (sin frontend web)
```

### "Puerto 8000 ocupado"
```
El launcher lo detectará y mostrará advertencia
Verifica: netstat -ano | findstr :8000
Mata el proceso: taskkill /PID <numero> /F
```

### "Error en migraciones"
```
Verifica que requirements-windows.txt existe
Borra backend/db.sqlite3 y backend/venv
Ejecuta MetricLab.bat de nuevo
```

### "No abre frontend"
```
Es normal si npm no está instalado
Puedes acceder al backend en http://localhost:8000/api
Instala Node.js y vuelve a ejecutar
```

---

## 🚀 **SIGUIENTES PASOS**

1. Ejecuta: `MetricLab.bat`
2. Abre navegador: `http://localhost:3000` (si npm) o `http://localhost:8000/api`
3. Crea un superuser (admin):
   ```
   python backend/manage.py createsuperuser
   ```
4. Accede a admin en: `http://localhost:8000/admin`

---

## 📝 **ARCHIVOS IMPORTANTES**

| Archivo | Propósito |
|---|---|
| `MetricLab.bat` | Launcher batch limpio (USAR ESTO) |
| `metriclab_launcher.py` | Launcher Python avanzado |
| `metriclab.spec` | Config PyInstaller para .exe |
| `backend/requirements-windows.txt` | Dependencias Python Windows |
| `backend/.env` | Variables de entorno |
| `BUILD_EXE.md` | Guía completa para construir .exe |

---

**¡MetricLab está listo para usar en Windows!**
