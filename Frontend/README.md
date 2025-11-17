# Frontend - Sistema de Gestión de Alquileres

Frontend desarrollado con React + Vite para el sistema de gestión de alquileres de vehículos.

## Tecnologías Utilizadas

- **React 18** - Librería de UI
- **React Router DOM** - Navegación entre páginas
- **Axios** - Cliente HTTP para comunicación con el backend
- **Recharts** - Gráficos y visualizaciones
- **date-fns** - Manejo de fechas
- **Vite** - Build tool y dev server

## Instalación

### Prerrequisitos

- Node.js 20.19.0 o superior
- npm 10.x o superior

### Pasos de instalación

1. Instalar las dependencias:

```bash
cd Frontend
npm install
```

## Ejecución en Desarrollo

1. Asegúrate de que el backend Flask esté corriendo en `http://localhost:5000`

2. Inicia el servidor de desarrollo:

```bash
npm run dev
```

3. Abre tu navegador en [http://localhost:3000](http://localhost:3000)

## Build para Producción

```bash
npm run build
```

## Módulos Disponibles

###  Implementados

- **Inicio** - Dashboard principal con acceso a todos los módulos
- **Vehículos** - CRUD completo de vehículos con validaciones

### = En Desarrollo

- **Clientes** - Gestión de clientes
- **Alquileres** - Alta, modificación y consulta de alquileres
- **Reservas** - Gestión de reservas anticipadas
- **Mantenimientos** - Control de mantenimientos de vehículos
- **Reportes** - Estadísticas y reportes con gráficos
