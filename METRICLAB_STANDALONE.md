# 🎯 MetricLab - Ejecutable Completo

## ¿QUÉ ES?

**MetricLab** es un sistema **STANDALONE COMPLETO** que detecta personas y evalúa su eficiencia laboral en tiempo real.

**Un único .exe que incluye:**
- ✅ Backend (Django REST API)
- ✅ Frontend (React con interfaz gráfica)
- ✅ Base de datos (SQLite)
- ✅ Detección de personas (MediaPipe + cámara)
- ✅ Evaluación de eficiencia
- ✅ Generación de reportes

---

## 🚀 CÓMO USAR

### **Opción 1: Ejecutable Portable (Recomendado)**

1. **Descargar:** `MetricLab.exe`
2. **Ejecutar:** Doble clic
3. **Listo:** Se abre la interfaz automáticamente

**Tamaño:** ~250 MB (incluye todo)
**Tiempo iniciación:** 5-10 segundos

### **Opción 2: Script Batch (Desarrollo)**

```batch
START_METRICLAB.bat
```

---

## 🎬 FUNCIONALIDADES

### Detección de Personas

| Característica | Descripción |
|---|---|
| 📷 Cámara en vivo | Acceso a webcam del dispositivo |
| 🧠 IA de detección | MediaPipe Face Detection |
| 👤 Identificación | Múltiples personas simultáneas |
| ⏱️ Tracking | Seguimiento continuo de personas |

### Evaluación de Eficiencia

| Métrica | Descripción |
|---|---|
| 👁️ Detección ocular | Ojos detectados/perdidos |
| 🧭 Orientación de cabeza | Orientación hacia pantalla |
| 😶 Distracción | Detección de desatención |
| ⚡ Puntuación atención | Score 0-100 de enfoque |
| 📊 Eficiencia laboral | % tiempo productivo vs inactivo |

### Dashboard

| Componente | Función |
|---|---|
| 📹 Visor en vivo | Video con overlay de detecciones |
| 📊 Gráficos reales | FPS, atención, tendencias |
| 📋 Reportes | Diarios, semanales, mensuales |
| 👥 Multi-usuario | Seguimiento de múltiples personas |
| 📈 Analytics | Análisis de tendencias |

---

## 🔄 FLUJO DE FUNCIONAMIENTO

```
┌─────────────────────────────────────────────┐
│  Ejecutar MetricLab.exe                     │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  1. Backend Django inicia                   │
│     (Puerto 8000, SQLite)                   │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  2. Frontend React inicia                   │
│     (Puerto 3000, interfaz gráfica)         │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  3. Navegador abre automáticamente          │
│     http://localhost:3000                   │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  4. Usuario hace clic: "Iniciar Cámara"    │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  5. Cámara se abre + MediaPipe              │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  6. Detección en vivo:                      │
│     - Detecta personas                      │
│     - Calcula eficiencia                    │
│     - Muestra overlay en video              │
│     - Guarda datos en BD                    │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  7. Reportes automáticos                    │
│     - Gráficos en tiempo real               │
│     - Estadísticas diarias/semanales        │
│     - Análisis de tendencias                │
└─────────────────────────────────────────────┘
```

---

## 📊 INTERFAZ PRINCIPAL

```
╔══════════════════════════════════════════════════════╗
║         MetricLab - Evaluación de Eficiencia        ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  ┌─────────────────────┐  ┌────────────────────┐   ║
║  │                     │  │ Métricas (TIEMPO   │   ║
║  │                     │  │ REAL):             │   ║
║  │   CÁMARA EN VIVO    │  │ • Personas: 2      │   ║
║  │   (Video + Overlay) │  │ • Atención: 87%    │   ║
║  │                     │  │ • Eficiencia: 92%  │   ║
║  │                     │  │ • FPS: 30          │   ║
║  └─────────────────────┘  └────────────────────┘   ║
║                                                      ║
║  ┌────────────────────────────────────────────┐    ║
║  │         GRÁFICOS Y ESTADÍSTICAS            │    ║
║  │ • Eficiencia por hora                      │    ║
║  │ • Atención promedio                        │    ║
║  │ • Tendencias semanales                     │    ║
║  └────────────────────────────────────────────┘    ║
║                                                      ║
║  [Iniciar Cámara] [Detener] [Reportes] [Salir]    ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

---

## 📝 REQUISITOS

### Mínimo
- **Windows 10/11** (64-bit)
- **Cámara web** (laptop o USB)
- **4GB RAM**

### Recomendado
- **Windows 10/11** (64-bit)
- **Cámara 1080p+**
- **8GB+ RAM**
- **Procesador i5+ o equivalente**

---

## 🎯 CASOS DE USO

### 1. Evaluación de Empleados
```
Gerente → Dashboard MetricLab
↓
Ve métricas de eficiencia en tiempo real
↓
Identifica momentos de baja productividad
↓
Toma decisiones basadas en datos
```

### 2. Monitoreo de Trabajo Remoto
```
Empleado trabaja en casa
↓
MetricLab rastrea eficiencia
↓
Genera reportes automáticos
↓
Empresa obtiene métricas verificables
```

### 3. Análisis de Capacitación
```
Personal en capacitación
↓
MetricLab mide atención durante sesión
↓
Reportes de distracción/enfoque
↓
Mejora de programas de capacitación
```

---

## 📊 SALIDA DE DATOS

### En Tiempo Real
- FPS (fotogramas por segundo)
- Personas detectadas
- Score de atención (0-100)
- Estado de ojos
- Orientación de cabeza

### Reportes Generados
- **Diarios:** Resumen de eficiencia del día
- **Semanales:** Tendencias y patrones
- **Mensuales:** Análisis comparativo
- **Por persona:** Detalles individuales

### Formatos de Exportación
- 📊 CSV (para Excel)
- 📈 PDF (para presentaciones)
- 📋 JSON (para sistemas externos)

---

## ⚙️ CONFIGURACIÓN

Ubicación: `%USERPROFILE%\.metriclab\`

```
.metriclab/
├── db.sqlite3          ← Base de datos
├── .env               ← Configuración
├── logs/              ← Archivos de log
└── reports/           ← Reportes generados
```

---

## 🔒 SEGURIDAD

- ✅ Contraseña para acceso (JWT)
- ✅ Datos locales (no nube)
- ✅ HTTPS en producción
- ✅ Encriptación de datos
- ✅ Control de acceso por roles

---

## 🐛 Troubleshooting

### "Cámara no abre"
```
Solución:
1. Settings > Privacy > Camera > Permitir acceso
2. Verificar que no esté bloqueada otra app
3. Reiniciar MetricLab
```

### "Muy lento"
```
Solución:
1. Cerrar otras aplicaciones
2. Actualizar drivers de cámara
3. Aumentar CPU available
```

### "Error de backend"
```
Solución:
1. Verificar puerto 8000 no esté en uso
2. Revisar antivirus/firewall
3. Ejecutar como administrador
```

---

## 🚀 PRÓXIMAS CARACTERÍSTICAS

- [ ] Detección de objetos (pantalla, documentos)
- [ ] Análisis de voz (interrupción de trabajo)
- [ ] Integración de calendario
- [ ] Notificaciones en tiempo real
- [ ] App móvil
- [ ] Multi-cámara

---

## 📞 SOPORTE

- 📧 Email: support@metriclab.local
- 🐛 Issues: GitHub Issues
- 📖 Documentación: docs/

---

**Versión**: 1.0 Standalone  
**Compilado**: 2026-06-07  
**Estado**: ✅ LISTO PARA PRODUCCIÓN
