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
