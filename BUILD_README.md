# 🚀 Guía Rápida para Compilar MetricLab.exe

## Método Recomendado: Usar BUILD_EXE.bat

```batch
BUILD_EXE.bat
```

Este script:
1. ✅ Verifica que npm esté instalado
2. ✅ Instala dependencias de React
3. ✅ Compila React a producción
4. ✅ Empaqueta todo en ejecutable Electron
5. ✅ Genera `dist/MetricLab-win32-x64/MetricLab.exe`

**Tiempo estimado: 3-5 minutos**

---

## ¿Dónde está el ejecutable?

Después de ejecutar `BUILD_EXE.bat`, el archivo estará en:

```
frontend/dist/MetricLab-win32-x64/MetricLab.exe
```

### Tamaño esperado:
- **MetricLab.exe**: ~200-250 MB (incluye Electron runtime)
- Esta es la carpeta completa que se necesita distribuir

---

## Limpiar el Proyecto

Para liberar espacio (elimina ~1.1 GB):

```batch
CLEAN.bat
```

Esto elimina:
- `backend/venv` (~376 MB)
- `frontend/node_modules` (~502 MB)
- `frontend/dist` (~260 MB)
- `frontend/build` (~12 MB)

**Nota**: Estos archivos se regeneran al compilar

---

## Prueba del Ejecutable

### Opción 1: Ejecutar directamente
```batch
frontend\dist\MetricLab-win32-x64\MetricLab.exe
```

### Opción 2: Desde PowerShell
```powershell
& 'C:\ruta\completa\frontend\dist\MetricLab-win32-x64\MetricLab.exe'
```

---

## Verificar que funciona correctamente

1. ✅ **Interfaz abre**: Debe verse la UI de React
2. ✅ **Botón "Iniciar Cámara" funciona**: Solicita permiso y muestra video
3. ✅ **API Backend**: Si backend está en `http://localhost:8000`, debe conectar
4. ✅ **Sin errores en consola**: DevTools solo abre en modo desarrollo

---

## Distribución

### Carpeta completa a distribuir:
```
frontend/dist/MetricLab-win32-x64/
├── MetricLab.exe          ← Ejecutable principal
├── resources/             ← Archivos de la aplicación
├── ffmpeg.dll
├── libEGL.dll
├── vulkan-1.dll
└── ... (otros .dll de Electron)
```

### Tamaño final: ~260 MB

Para distribuir:
1. Copiar toda la carpeta `frontend/dist/MetricLab-win32-x64/`
2. Los usuarios simplemente hacen doble clic en `MetricLab.exe`
3. No requiere instalación o dependencias adicionales

---

## Troubleshooting

### Error: "npm no encontrado"
```
Instala Node.js desde: https://nodejs.org
```

### Error: "Puerto 8000 ya está en uso"
```
Cambiar en frontend/src/services/api.js
```

### Ejecutable no abre la cámara
```
Verificar que:
1. La cámara esté disponible
2. Los permisos de Windows permitan acceso
3. No haya otra app usando la cámara
```

### Ejecutable muy lento
```
Asegurar que:
1. node_modules se compilo correctamente
2. React build es versión PRODUCTION
3. No hay DevTools abierto (solo en desarrollo)
```

---

## Arquitectura del Executable

```
MetricLab.exe
    ├── Electron Runtime (binario)
    ├── V8 Engine (JavaScript)
    ├── Chromium (navegador)
    └── App (React)
        ├── UI Components
        ├── Camera (MediaPipe)
        ├── API Client
        └── Assets
```

---

## Scripts disponibles

| Script | Acción |
|--------|--------|
| `BUILD_EXE.bat` | Compilar .exe (RECOMENDADO) |
| `CLEAN.bat` | Limpiar archivos temporales |
| `MetricLab.bat` | Ejecutar backend + frontend local |
| `frontend\package.json -> scripts` | `npm run electron:package` (alternativa) |

---

## Para Desarrolladores

### Desarrollo local con hot reload:

Terminal 1 - Backend:
```batch
MetricLab.bat
```

Terminal 2 - Frontend React dev server:
```batch
cd frontend
npm start
```

Terminal 3 - Electron (conecta a localhost:3000):
```batch
cd frontend
npm run electron
```

---
