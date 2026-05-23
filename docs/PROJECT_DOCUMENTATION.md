# Documentación del Proyecto

## 1. Documento de Visión del Proyecto

### 1.1 Objetivo del sistema
El sistema es una plataforma de monitoreo de eficiencia laboral diseñada para registrar, analizar y reportar horas trabajadas, actividades ejecutadas y patrones de productividad.

### 1.2 Problema que resuelve
Resuelve la falta de visibilidad sobre el uso del tiempo y el desempeño de empleados, permitiendo a gerentes y administradores identificar inactividad, tiempo perdido y oportunidades de mejora.

### 1.3 Alcance
El sistema cubre el registro de horas, seguimiento de actividades, generación de reportes de eficiencia y análisis de tendencias de uso laboral.

### 1.4 Usuarios
- **Administrador**: configura el sistema, gestiona usuarios y accede a reportes globales.
- **Gerente**: supervisa equipos, revisa métricas y toma decisiones basadas en informes.
- **Empleado**: reporta su tiempo, revisa su desempeño y accede a su historial.

### 1.5 Beneficios
- Mejora de la visibilidad operativa.
- Detección temprana de inactividad o baja productividad.
- Generación de decisiones basadas en datos.
- Aumento de la eficiencia en la gestión de recursos humanos.

### 1.6 Metas
- Implementar un sistema funcional de tracking de tiempo.
- Generar reportes diarios, semanales y mensuales.
- Entregar dashboards claros para gerentes y empleados.
- Garantizar seguridad y privacidad en el tratamiento de datos.

## 1.2 Estudio de Viabilidad

### Viabilidad técnica
El proyecto utiliza tecnologías probadas: Django, React, PostgreSQL y Docker. El desarrollo es viable con el equipo actual y los lenguajes elegidos.

### Viabilidad económica
El costo se concentra en la infraestructura, licencias opcionales y horas de desarrollo. El retorno se espera por la mejora en la productividad y la reducción de desperdicio de tiempo.

### Viabilidad operativa
El sistema puede integrarse en entornos empresariales con prácticas de monitoreo ya existentes, respetando los procedimientos internos de cada organización.

### Viabilidad legal
Se debe considerar cumplimiento de privacidad laboral y protección de datos personales. El sistema debe ser configurable para cumplir leyes locales y políticas internas de la empresa.

### Viabilidad tecnológica
La arquitectura es compatible con despliegue en la nube o en servidores locales. Se puede ampliar con módulos adicionales sin rehacer la base.

## 1.3 Alcance del Proyecto

### Qué hará el sistema
- Registro de sesiones de trabajo.
- Detección de inactividad y pausas.
- Generación de reportes de productividad.
- Gestión de usuarios y roles.
- Visualización de métricas y tendencias.

### Qué NO hará el sistema
- No realizará evaluaciones psicológicas de empleados.
- No monitorizará contenido de archivos ni comunicaciones privadas.
- No actuará como herramienta de vigilancia intrusiva fuera del horario laboral.

### Límites del proyecto
El alcance cubre solo el registro de actividad laboral y reportes de eficiencia; no incluye auditoría de contenido ni integración inmediata con sistemas de video vigilancia.

### Módulos incluidos
- Autenticación y autorización.
- Tracking de tiempo.
- Reportes y dashboards.
- Gestión de usuarios.
- API REST.

## 2. Documentación de Requerimientos

### 2.1 Requerimientos Funcionales
- Registrar horarios de inicio y fin de jornada.
- Detectar inactividad del usuario.
- Generar reportes diarios, semanales y mensuales.
- Calcular índices de productividad.
- Permitir autenticación segura.
- Definir roles con permisos específicos.
- Exportar métricas en formatos comunes.

### 2.2 Requerimientos No Funcionales
- Seguridad: protección de datos y acceso controlado.
- Rendimiento: respuesta de API en menos de 500ms para consultas comunes.
- Escalabilidad: soportar múltiples usuarios concurrentes.
- Disponibilidad: mantenimiento de servicio en un 99%.
- Usabilidad: interfaz clara y accesible.
- Compatibilidad: funcionar en navegadores modernos.

### 2.3 Historias de Usuario
- Como supervisor, quiero visualizar el tiempo inactivo de los empleados para detectar pérdidas de productividad.
- Como gerente, quiero revisar reportes semanales para tomar decisiones de asignación de recursos.
- Como empleado, quiero ver mi historial de horas para validar mi desempeño.
- Como administrador, quiero gestionar usuarios y permisos para mantener el control del sistema.

### 2.4 Casos de Uso
- Iniciar sesión.
- Registrar actividad o pausa.
- Generar reporte de productividad.
- Exportar métricas.
- Consultar historial de tiempos.
- Gestionar usuarios y roles.

## 3. Documentación de Análisis y Diseño

### 3.1 Diagrama de Arquitectura
La arquitectura incluye:
- Frontend React.
- Backend Django REST.
- API REST.
- Base de datos PostgreSQL.
- Cliente de escritorio o web.
- Docker y Nginx como infraestructura de despliegue.

> Ver también: [ARQUITECTURA.md](../ARQUITECTURA.md)

### 3.2 Modelo Entidad-Relación (ERD)
Tablas principales previstas:
- Empleados
- Actividades
- Sesiones
- Métricas
- Departamentos
- Reportes

### 3.3 Diagramas UML
- Casos de Uso: mapeo de acciones por usuario.
- Diagramas de Clases: estructura del dominio.
- Diagramas de Secuencia: flujo de generación de reportes y login.
- Diagramas de Actividad: procesos de registro y análisis.

### 3.4 Diseño de Base de Datos
El modelo incluye tablas, claves primarias/foráneas, relaciones y normalización para evitar redundancia.
- Empleados: nombre, email, rol.
- Actividades: tipo, duración, categoría.
- Sesiones: inicio, fin, estado.
- Reportes: resumen de métricas.

### 3.5 Diseño de API REST
Endpoints principales:
- `POST /login`
- `GET /employees`
- `POST /activity`
- `GET /reports`
- `GET /analytics/efficiency`

### 3.6 Diseño de UI/UX
Mockups principales:
- Login.
- Dashboard ejecutivo.
- Panel de métricas.
- Panel administrativo.

Herramientas sugeridas:
- Figma.
- Adobe XD.

## 4. Documentación Técnica

### 4.1 Documento de Arquitectura de Software
Incluye:
- Tecnologías usadas.
- Capas de la aplicación.
- Comunicación entre frontend y backend.
- Patrones arquitectónicos.
- Requisitos de seguridad.

### 4.2 Manual Técnico
Para desarrolladores:
- Instalación.
- Configuración.
- Despliegue.
- Estructura del código.
- Convenciones del proyecto.

### 4.3 Documentación de APIs
Describir cada endpoint con Swagger/OpenAPI para mantener una referencia profesional.

## 5. Documentación de Gestión

### 5.1 Cronograma del Proyecto
Fases sugeridas:
- Análisis.
- Diseño.
- Desarrollo.
- Pruebas.
- Despliegue.

Herramientas sugeridas:
- Gantt.
- Jira.
- Trello.

### 5.2 Gestión de Riesgos
Riesgos identificados:
- Fuga de datos.
- Errores de monitoreo.
- Caída del servidor.
- Problemas legales por privacidad.

### 5.3 Presupuesto
Incluye costos de infraestructura, licencias, horas de desarrollo y mantenimiento.

## 6. Documentación de Pruebas

### 6.1 Plan de Pruebas
Define:
- Qué se probará.
- Metodología.
- Criterios de aceptación.

### 6.2 Casos de Prueba
Ejemplo:
- **Caso**: Login correcto
  - **Resultado esperado**: Acceso permitido.
- **Caso**: Usuario inválido
  - **Resultado esperado**: Error mostrado.

### 6.3 Reportes de Bugs
Seguimiento de errores y estado de corrección.

## 7. Documentación de Seguridad

### 7.1 Política de Seguridad
Define controles de acceso, permisos, cifrado y auditoría.

### 7.2 Política de Privacidad
Incluye tratamiento de datos sensibles, actividad laboral y cumplimiento legal.

## 8. Documentación Final

### 8.1 Manual de Usuario
Guía de uso para usuarios finales y administradores.

### 8.2 Informe Final del Proyecto
Resumen completo con:
- Objetivos.
- Arquitectura.
- Resultados.
- Conclusiones.
