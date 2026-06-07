# Frontend React - Time Tracker

## Setup

1. **Instalar dependencias**
```bash
npm install
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
```

3. **Iniciar servidor de desarrollo**
```bash
npm start
```

La aplicación estará en: `http://localhost:3000`

## Scripts Disponibles

```bash
npm start           # Iniciar servidor de desarrollo
npm test            # Ejecutar tests
npm run build       # Build para producción
npm run eject       # Eject create-react-app (irreversible)
npm run lint        # Ejecutar ESLint
npm run format      # Formatear código con Prettier
```

## Estructura

```
frontend/
├── src/
│   ├── components/      # Componentes reutilizables
│   ├── pages/          # Páginas principales
│   ├── services/       # Servicios API
│   ├── redux/          # Gestión de estado
│   ├── styles/         # Estilos globales
│   ├── utils/          # Utilidades
│   ├── App.js
│   └── index.js
├── public/
├── package.json
└── .env.example
```

## Testing

```bash
npm test
npm test -- --coverage
```

## Build

```bash
npm run build
```

Los archivos optimizados estarán en la carpeta `build/`

## Ejecutable de escritorio (Electron)

Este proyecto ahora incluye un envoltorio de escritorio para ejecutar el frontend como aplicación local.

1. Instala dependencias:
```bash
npm install
```

2. Ejecuta el backend Django en `http://localhost:8000`.

3. En otra terminal, ejecuta el frontend en modo de desarrollo:
```bash
npm start
```

4. Abre otra terminal para lanzar la aplicación Electron:
```bash
set "ELECTRON_START_URL=http://localhost:3000" && npm run electron
```

5. Para generar la versión de producción y abrirla en Electron:
```bash
npm run electron:build
```

6. Para empaquetar un ejecutable de Windows:
```bash
npm run electron:package
```

El paquete se generará en `frontend/dist/MetricLab-win32-x64`.

> Nota: la cámara del dispositivo se muestra al hacer clic en el botón `📹 Iniciar Cámara` dentro de la interfaz.
