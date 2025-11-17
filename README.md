# Sistema de Gestión de Alquileres de Vehículos

## Materia: Desarrollo de Aplicaciones con Objetos

**Proyecto académico** que demuestra la aplicación de conceptos fundamentales de Programación Orientada a Objetos en un sistema real de gestión de alquileres.

---

## 📋 Descripción del Proyecto

Sistema completo de gestión de alquileres de vehículos que implementa:

- ✅ Interfaz web moderna (React + Vite)
- ✅ API RESTful (Flask + Python)
- ✅ Base de datos relacional (SQLite)
- ✅ Operaciones CRUD completas
- ✅ **Conceptos avanzados de POO**
- ✅ **Patrones de diseño**

---

## 🎓 Conceptos de POO Implementados

### 1. **Herencia**
- `BaseRepository` - Clase base abstracta para todos los repositorios
- `Persona` - Clase base para Cliente y Empleado
- Ver: [`Backend/app/repository/BaseRepository.py`](Backend/app/repository/BaseRepository.py)

### 2. **Polimorfismo**
- Método `to_dict()` implementado de forma diferente en cada modelo
- Método `calcular()` con diferentes algoritmos en estrategias de tarifa
- Ver: [`Backend/app/models/strategies/TarifaStrategy.py`](Backend/app/models/strategies/TarifaStrategy.py)

### 3. **Abstracción**
- Clases abstractas con `ABC` (Abstract Base Class)
- Métodos abstractos que obligan a implementación en subclases
- Ver: [`Backend/app/models/Persona.py`](Backend/app/models/Persona.py)

### 4. **Encapsulamiento**
- Atributos privados/protegidos con prefijo `_`
- Properties con getters y setters
- Validación de datos en setters
- Ver: [`Backend/app/models/Persona.py`](Backend/app/models/Persona.py) líneas 25-65

### 5. **Composición**
- `CalculadoraTarifa` TIENE-UN `TarifaStrategy`
- Ver: [`Backend/app/models/strategies/TarifaStrategy.py`](Backend/app/models/strategies/TarifaStrategy.py) líneas 165-195

### 6. **Patrones de Diseño**

#### Strategy Pattern
- Diferentes algoritmos de cálculo de tarifa intercambiables
- Ver: [`Backend/app/models/strategies/TarifaStrategy.py`](Backend/app/models/strategies/TarifaStrategy.py)

#### Factory Pattern
- Creación centralizada de objetos estrategia y repositorios
- Ver: [`Backend/app/models/factories/TarifaFactory.py`](Backend/app/models/factories/TarifaFactory.py)

#### Repository Pattern
- Abstracción del acceso a datos
- Ver: [`Backend/app/repository/`](Backend/app/repository/)

---

## 📁 Estructura del Proyecto

```
TP_DAO/
│
├── Backend/ (Python + Flask)
│   ├── app/
│   │   ├── database/
│   │   │   ├── database.py        # Conexión a BD
│   │   │   ├── init_db.py         # Creación de tablas
│   │   │   └── seed_data.py       # Datos de ejemplo
│   │   │
│   │   ├── models/                # Modelos de datos
│   │   │   ├── Persona.py         # ⭐ Clase base abstracta
│   │   │   ├── Cliente.py
│   │   │   ├── Vehiculo.py
│   │   │   ├── Alquiler.py
│   │   │   │
│   │   │   ├── strategies/        # ⭐ Strategy Pattern
│   │   │   │   └── TarifaStrategy.py
│   │   │   │
│   │   │   └── factories/         # ⭐ Factory Pattern
│   │   │       └── TarifaFactory.py
│   │   │
│   │   ├── repository/            # ⭐ Repository Pattern
│   │   │   ├── BaseRepository.py  # Clase base abstracta
│   │   │   ├── VehiculoRepository.py
│   │   │   └── ClienteRepository.py
│   │   │
│   │   ├── services/              # Lógica de negocio
│   │   │   ├── VehiculoService.py
│   │   │   └── ClienteService.py
│   │   │
│   │   └── routes/                # Endpoints REST
│   │       ├── Vehiculo.py
│   │       └── Cliente.py
│   │
│   └── ejemplos_poo.py            # ⭐ Ejemplos ejecutables de POO
│
├── Frontend/ (React + Vite)
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/           # Componentes reutilizables
│   │   │   └── layout/           # Layout de la app
│   │   │
│   │   ├── pages/
│   │   │   ├── Vehiculos/        # ✅ Módulo completo
│   │   │   ├── Clientes/         # ✅ Módulo completo
│   │   │   ├── Alquileres/
│   │   │   ├── Reservas/
│   │   │   ├── Mantenimientos/
│   │   │   └── Reportes/
│   │   │
│   │   └── services/             # API clients
│   │
│   └── package.json
│
├── CONCEPTOS_POO.md              # ⭐ Documentación detallada de POO
├── INSTRUCCIONES_EJECUCION.md    # Guía de instalación y ejecución
└── README.md                      # Este archivo
```

---

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.12+
- Node.js 20.19+
- npm 10.x+

### Backend (Terminal 1)

```bash
cd Backend

# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos
python app/database/init_db.py

# Insertar datos de ejemplo
python app/database/seed_data.py

# Ejecutar servidor
python -m app.main
```

Backend disponible en: **http://localhost:5000**

### Frontend (Terminal 2)

```bash
cd Frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

Frontend disponible en: **http://localhost:3000**

---

## 🧪 Ejecutar Ejemplos de POO

Para ver en acción los conceptos de POO implementados:

```bash
cd Backend
python ejemplos_poo.py
```

Esto ejecutará ejemplos de:
- ✅ Strategy Pattern
- ✅ Factory Pattern
- ✅ Polimorfismo
- ✅ Composición
- ✅ Casos prácticos de uso

---

## 📚 Documentación de Conceptos de POO

Ver el archivo [**CONCEPTOS_POO.md**](CONCEPTOS_POO.md) para documentación detallada que incluye:

- Explicación de cada concepto de POO
- Ubicación exacta en el código (archivos y líneas)
- Diagramas de clases
- Ejemplos de uso
- Beneficios de cada patrón

---

## 🎯 Funcionalidades Implementadas

### Módulos Completos

#### 1. Gestión de Vehículos ✅
- CRUD completo (Crear, Leer, Actualizar, Eliminar)
- Validaciones de datos
- Campos: Patente, Marca, Modelo, Año, Tarifa, KM, Vencimientos

#### 2. Gestión de Clientes ✅
- CRUD completo
- Validación de email
- Campos: DNI, Nombre, Apellido, Email, Teléfono, Licencia

#### 3. Base de Datos
- 8 vehículos de ejemplo
- 3 clientes de ejemplo
- 3 empleados de ejemplo
- Estados inicializados

### En Desarrollo
- Módulo de Alquileres
- Módulo de Reservas
- Módulo de Mantenimientos
- Módulo de Reportes con gráficos

---

## 🔑 Características Técnicas

### Backend
- **Framework:** Flask 3.0.3
- **Base de Datos:** SQLite
- **Arquitectura:** MVC con capas (Models, Repository, Services, Routes)
- **Patrones:** Repository, Strategy, Factory
- **CORS:** Habilitado para desarrollo

### Frontend
- **Framework:** React 18.3.1
- **Build Tool:** Vite 6.0.3
- **Router:** React Router DOM 6.28.0
- **HTTP Client:** Axios 1.7.7
- **Gráficos:** Recharts 2.15.0 (preparado)

---

## 📊 Arquitectura del Sistema

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
         │   - Components         │
         │   - Services (Axios)   │
         └───────────┬────────────┘
                     │
                     │ API Calls
                     │
         ┌───────────▼────────────┐
         │   BACKEND (Flask)      │
         │   ┌────────────┐       │
         │   │  Routes    │       │  ← REST API
         │   └─────┬──────┘       │
         │   ┌─────▼──────┐       │
         │   │  Services  │       │  ← Lógica de Negocio
         │   └─────┬──────┘       │  ← Strategy Pattern
         │   ┌─────▼──────┐       │
         │   │ Repository │       │  ← Repository Pattern
         │   └─────┬──────┘       │  ← Herencia de BaseRepository
         │         │              │
         └─────────┼──────────────┘
                   │
         ┌─────────▼──────────┐
         │   SQLite Database  │
         └────────────────────┘
```

---

## 🎓 Conceptos de POO por Archivo

### Archivos Clave con Conceptos de POO

| Archivo | Conceptos Aplicados | Importancia |
|---------|-------------------|-------------|
| `BaseRepository.py` | Herencia, Abstracción, Generics | ⭐⭐⭐ |
| `Persona.py` | Herencia, Encapsulamiento, Abstracción | ⭐⭐⭐ |
| `TarifaStrategy.py` | Strategy Pattern, Polimorfismo | ⭐⭐⭐ |
| `TarifaFactory.py` | Factory Pattern, Encapsulamiento | ⭐⭐⭐ |
| `CalculadoraTarifa` | Composición (HAS-A) | ⭐⭐ |

---

## 📝 Ejemplos de Código

### Ejemplo 1: Herencia con BaseRepository

```python
# Clase base abstracta
class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def crear(self, entidad: T) -> T:
        pass

# Subclase que hereda e implementa
class VehiculoRepository(BaseRepository[Vehiculo]):
    def crear(self, vehiculo: Vehiculo) -> Vehiculo:
        # Implementación específica
        query = "INSERT INTO vehiculos ..."
        # ...
```

### Ejemplo 2: Strategy Pattern

```python
# Diferentes estrategias de cálculo
calculadora = CalculadoraTarifa(TarifaSimple())
monto1 = calculadora.calcular_monto(5000, fecha1, fecha2)

# Cambiar estrategia en tiempo de ejecución
calculadora.cambiar_estrategia(TarifaPremium())
monto2 = calculadora.calcular_monto(5000, fecha1, fecha2)
```

### Ejemplo 3: Factory Pattern

```python
# Crear objetos sin conocer las clases concretas
estrategia = TarifaFactory.crear_estrategia('premium', costo_por_km=30)
```

---

## 🧪 Testing

Para probar los conceptos de POO:

```bash
# Ejecutar ejemplos interactivos
python Backend/ejemplos_poo.py
```

---

## 📖 Referencias y Recursos

- **Documentación POO:** [`CONCEPTOS_POO.md`](CONCEPTOS_POO.md)
- **Guía de Ejecución:** [`INSTRUCCIONES_EJECUCION.md`](INSTRUCCIONES_EJECUCION.md)
- **Frontend Docs:** [`Frontend/README.md`](Frontend/README.md)

---

## 👥 Autores

**Proyecto académico** para la materia Desarrollo de Aplicaciones con Objetos

---

## 📄 Licencia

Este proyecto es de uso académico y educativo.

---

## 🌟 Conceptos Destacados para Evaluación

### ✅ Herencia
- Implementada en `BaseRepository` y `Persona`
- Ver archivos en `Backend/app/repository/` y `Backend/app/models/`

### ✅ Polimorfismo
- Método `calcular()` con diferentes implementaciones
- Método `to_dict()` en todos los modelos

### ✅ Abstracción
- Clases abstractas con `ABC`
- Métodos abstractos que fuerzan implementación

### ✅ Encapsulamiento
- Atributos privados con properties
- Validación en setters

### ✅ Composición
- `CalculadoraTarifa` contiene `TarifaStrategy`
- Relación HAS-A en lugar de IS-A

### ✅ Patrones de Diseño
- **Strategy Pattern** - Algoritmos intercambiables
- **Factory Pattern** - Creación centralizada
- **Repository Pattern** - Abstracción de datos

---

**Ver [`CONCEPTOS_POO.md`](CONCEPTOS_POO.md) para documentación completa y detallada.**
