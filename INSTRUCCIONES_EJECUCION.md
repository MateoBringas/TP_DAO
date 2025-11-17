# Instrucciones de Ejecución - Sistema de Gestión de Alquileres

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                   NAVEGADOR WEB                         │
│              http://localhost:3000                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTP Requests (JSON)
                     │
         ┌───────────▼────────────┐
         │   FRONTEND (React)     │
         │   Puerto: 3000         │
         │   - React Router       │
         │   - Axios              │
         │   - Recharts           │
         └───────────┬────────────┘
                     │
                     │ API Calls
                     │
         ┌───────────▼────────────┐
         │   BACKEND (Flask)      │
         │   Puerto: 5000         │
         │   - Flask-CORS         │
         │   - SQLite             │
         └───────────┬────────────┘
                     │
                     │
         ┌───────────▼────────────┐
         │   BASE DE DATOS        │
         │   SQLite (database.db) │
         └────────────────────────┘
```

## Paso 1: Configurar el Backend

### 1.1 Navegar al directorio del backend

```bash
cd Backend
```

### 1.2 Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

Dependencias instaladas:
- Flask 3.0.3
- flask-cors 3.0.10

### 1.3 Inicializar la base de datos (si no existe)

```bash
python app/database/init_db.py
```

Esto creará:
- El archivo `database.db` con todas las tablas
- Datos iniciales si los hay

### 1.4 Ejecutar el servidor Flask

```bash
python -m app.main
```

O también:

```bash
python app/main.py
```

El backend estará disponible en: **http://localhost:5000**

Deberías ver un mensaje similar a:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

## Paso 2: Configurar el Frontend

### 2.1 Abrir una NUEVA terminal (dejar el backend corriendo)

### 2.2 Navegar al directorio del frontend

```bash
cd Frontend
```

### 2.3 Instalar dependencias de Node.js

```bash
npm install
```

Esto instalará:
- React 18.3.1
- React Router DOM 6.28.0
- Axios 1.7.7
- Recharts 2.15.0
- date-fns 4.1.0
- Vite 6.0.3

**Nota**: Si hay advertencias de versión de Node, puedes continuar igual. El proyecto funciona con Node.js v22.11.0

### 2.4 Ejecutar el servidor de desarrollo

```bash
npm run dev
```

El frontend estará disponible en: **http://localhost:3000**

Deberías ver un mensaje similar a:
```
  VITE v6.0.3  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### 2.5 Abrir en el navegador

Abre tu navegador en: **http://localhost:3000**

## Paso 3: Verificar la Conexión

1. En el navegador, deberías ver la página de inicio con 6 módulos:
   - 🏠 Inicio
   - 🚗 Vehículos
   - 👥 Clientes
   - 📋 Alquileres
   - 📅 Reservas
   - 🔧 Mantenimientos
   - 📊 Reportes

2. Haz clic en "Vehículos" para probar el módulo implementado

3. Si hay errores de conexión, verifica:
   - ✅ Backend corriendo en puerto 5000
   - ✅ Frontend corriendo en puerto 3000
   - ✅ No hay errores en las consolas

## Estructura de Archivos

```
TP_DAO/
│
├── Backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database/
│   │   │   ├── database.py
│   │   │   └── init_db.py
│   │   ├── models/
│   │   │   ├── Vehiculo.py
│   │   │   ├── Cliente.py
│   │   │   ├── Alquiler.py
│   │   │   ├── Reserva.py
│   │   │   ├── Mantenimiento.py
│   │   │   ├── Incidente.py
│   │   │   └── states/
│   │   ├── repository/
│   │   │   ├── VehiculoRepository.py
│   │   │   ├── ClienteRepository.py
│   │   │   └── ...
│   │   ├── services/
│   │   │   └── VehiculoService.py
│   │   └── routes/
│   │       └── Vehiculo.py
│   └── requirements.txt
│
└── Frontend/
    ├── src/
    │   ├── components/
    │   │   ├── common/      # Componentes reutilizables
    │   │   └── layout/      # Layout de la app
    │   ├── pages/
    │   │   ├── Home/
    │   │   ├── Vehiculos/   # ✅ Implementado
    │   │   ├── Clientes/
    │   │   ├── Alquileres/
    │   │   ├── Reservas/
    │   │   ├── Mantenimientos/
    │   │   └── Reportes/
    │   ├── services/        # API clients
    │   ├── styles/
    │   ├── App.jsx
    │   └── main.jsx
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## Funcionalidades Implementadas

### ✅ Backend
- Estructura MVC completa
- Modelos de datos para todas las entidades
- Endpoints de Vehículos (GET, POST)
- Base de datos SQLite
- CORS habilitado

### ✅ Frontend
- Aplicación React con Vite
- Sistema de navegación con React Router
- Layout responsivo con sidebar
- Módulo de Vehículos completo (CRUD)
- Componentes reutilizables (Button, Input, Table, Modal)
- Servicios API para todas las entidades
- Estilos modernos y responsivos

## Próximos Pasos Sugeridos

1. **Completar endpoints del backend**:
   - Agregar rutas para Clientes
   - Agregar rutas para Alquileres
   - Agregar rutas para Reservas
   - Agregar rutas para Mantenimientos
   - Agregar endpoints de Reportes

2. **Implementar módulos del frontend**:
   - Módulo de Clientes (similar a Vehículos)
   - Módulo de Alquileres
   - Módulo de Reservas
   - Módulo de Mantenimientos
   - Módulo de Reportes con gráficos

3. **Mejoras adicionales**:
   - Validaciones avanzadas
   - Autenticación de usuarios
   - Exportación de reportes a PDF/Excel
   - Notificaciones push
   - Tests unitarios

## Solución de Problemas

### Error: "Cannot connect to backend"
- Verifica que el backend esté corriendo en puerto 5000
- Revisa la consola del backend por errores

### Error: "Module not found"
- Ejecuta `npm install` en la carpeta Frontend
- Verifica que todas las dependencias estén instaladas

### Puerto 3000 o 5000 ocupado
- Backend: Cambia el puerto en `app/main.py`
- Frontend: Cambia el puerto en `vite.config.js`

### CORS Error
- Verifica que `flask-cors` esté instalado
- Verifica que CORS esté habilitado en `app/__init__.py`

## Contacto

Para preguntas o asistencia, contacta al equipo de desarrollo.
