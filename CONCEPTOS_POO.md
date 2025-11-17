# Conceptos de Programación Orientada a Objetos Aplicados

## Materia: Desarrollo de Aplicaciones con Objetos

Este documento detalla todos los conceptos de POO implementados en el sistema de gestión de alquileres de vehículos.

---

## 📚 Índice de Conceptos Implementados

1. [Herencia](#1-herencia)
2. [Polimorfismo](#2-polimorfismo)
3. [Abstracción](#3-abstracción)
4. [Encapsulamiento](#4-encapsulamiento)
5. [Composición](#5-composición)
6. [Patrones de Diseño](#6-patrones-de-diseño)
   - Strategy Pattern
   - Factory Pattern
   - Repository Pattern

---

## 1. Herencia

### 1.1 BaseRepository - Clase Abstracta Base para Repositorios

**Ubicación:** `Backend/app/repository/BaseRepository.py`

**Descripción:** Clase abstracta que define la estructura común para todos los repositorios del sistema.

```python
class BaseRepository(ABC, Generic[T]):
    """Clase base abstracta para todos los repositorios"""

    @abstractmethod
    def crear(self, entidad: T) -> T:
        pass

    @abstractmethod
    def obtener_todos(self) -> List[T]:
        pass

    # ... más métodos abstractos
```

**Subclases que heredan:**
- `VehiculoRepository` hereda de `BaseRepository`
- `ClienteRepository` hereda de `BaseRepository`
- `AlquilerRepository` hereda de `BaseRepository`

**Beneficios:**
- ✅ Reutilización de código
- ✅ Estructura común para todos los repositorios
- ✅ Garantiza que todos implementen los métodos CRUD básicos

---

### 1.2 Persona - Jerarquía de Herencia

**Ubicación:** `Backend/app/models/Persona.py`

**Descripción:** Clase abstracta base para representar personas en el sistema.

```python
class Persona(ABC):
    """Clase base abstracta para personas"""

    def __init__(self, nombre, apellido, dni, email, telefono, habilitado):
        self._nombre = nombre
        self._apellido = apellido
        # ... más atributos comunes

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def get_tipo(self) -> str:
        pass
```

**Jerarquía de Herencia:**
```
Persona (abstracta)
    ├── Cliente
    └── Empleado
```

**Características:**
- Atributos comunes: nombre, apellido, DNI, email, teléfono
- Métodos comunes: `get_nombre_completo()`, `__str__()`, `__repr__()`
- Métodos abstractos que deben implementar las subclases

---

## 2. Polimorfismo

### 2.1 Polimorfismo en to_dict()

**Ubicación:** Todos los modelos (`Cliente.py`, `Vehiculo.py`, `Alquiler.py`, etc.)

**Descripción:** Cada clase implementa su propia versión del método `to_dict()`.

```python
# En Cliente
def to_dict(self):
    return {
        "id_cliente": self.id_cliente,
        "dni": self.dni,
        "nombre": self.nombre,
        # ... campos específicos de Cliente
    }

# En Vehiculo
def to_dict(self):
    return {
        "id_vehiculo": self.id_vehiculo,
        "patente": self.patente,
        "marca": self.marca,
        # ... campos específicos de Vehículo
    }
```

**Beneficio:** Mismo método, comportamiento diferente según la clase.

---

### 2.2 Polimorfismo en Estrategias de Tarifa

**Ubicación:** `Backend/app/models/strategies/TarifaStrategy.py`

**Descripción:** Diferentes clases implementan el mismo método `calcular()` de formas distintas.

```python
# TarifaSimple
def calcular(self, tarifa_base, fecha_inicio, fecha_fin, km_recorridos=0):
    dias = (fecha_fin - fecha_inicio).days
    return tarifa_base * dias

# TarifaConDescuentoSemanal
def calcular(self, tarifa_base, fecha_inicio, fecha_fin, km_recorridos=0):
    dias = (fecha_fin - fecha_inicio).days
    monto = tarifa_base * dias
    if dias >= 7:
        monto = monto * 0.90  # 10% descuento
    return monto

# TarifaPorKilometraje
def calcular(self, tarifa_base, fecha_inicio, fecha_fin, km_recorridos=0):
    dias = (fecha_fin - fecha_inicio).days
    monto_base = tarifa_base * dias
    costo_km = km_recorridos * self.costo_por_km
    return monto_base + costo_km
```

**Beneficio:** Diferentes algoritmos de cálculo intercambiables.

---

## 3. Abstracción

### 3.1 Clases Abstractas (ABC)

**Clases abstractas implementadas:**

1. **BaseRepository** (`BaseRepository.py`)
   - Define interfaz común para repositorios
   - No puede instanciarse directamente
   - Obliga a subclases a implementar métodos CRUD

2. **Persona** (`Persona.py`)
   - Define estructura común para Cliente y Empleado
   - Métodos abstractos: `to_dict()`, `get_tipo()`

3. **TarifaStrategy** (`TarifaStrategy.py`)
   - Define interfaz para estrategias de cálculo
   - Método abstracto: `calcular()`

**Ejemplo de uso:**

```python
from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    def crear(self, entidad):
        """Método que DEBE ser implementado por subclases"""
        pass
```

**Beneficio:** Oculta detalles de implementación, solo expone interfaz.

---

## 4. Encapsulamiento

### 4.1 Atributos Privados y Protegidos

**Ubicación:** `Backend/app/models/Persona.py`

**Descripción:** Uso de atributos privados (prefijo `_`) con getters y setters.

```python
class Persona(ABC):
    def __init__(self, nombre, apellido, ...):
        self._nombre = nombre      # Atributo protegido
        self._apellido = apellido  # Atributo protegido
        self._dni = dni

    # GETTER
    @property
    def nombre(self) -> str:
        return self._nombre

    # SETTER con validación
    @nombre.setter
    def nombre(self, valor: str):
        if not valor or valor.strip() == "":
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor.strip()
```

**Beneficios:**
- ✅ Validación de datos antes de asignar
- ✅ Control sobre cómo se accede a los atributos
- ✅ Protección de la integridad de los datos

---

### 4.2 Encapsulamiento en Repository

**Ubicación:** `Backend/app/repository/BaseRepository.py`

```python
class BaseRepository(ABC):
    def __init__(self, connection_factory=get_connection):
        self._connection_factory = connection_factory  # Privado

    def ejecutar_query(self, query, parametros=None):
        """Método que encapsula la lógica de conexión a BD"""
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            # Lógica encapsulada
```

**Beneficio:** La lógica de conexión está oculta, solo se expone la interfaz pública.

---

## 5. Composición

### 5.1 CalculadoraTarifa - Composición de Estrategias

**Ubicación:** `Backend/app/models/strategies/TarifaStrategy.py`

**Descripción:** La clase `CalculadoraTarifa` **contiene** una instancia de `TarifaStrategy`.

```python
class CalculadoraTarifa:
    """COMPOSICIÓN: Contiene una estrategia"""

    def __init__(self, estrategia: TarifaStrategy):
        self._estrategia = estrategia  # TIENE-UN

    def cambiar_estrategia(self, estrategia: TarifaStrategy):
        """Cambia la estrategia en tiempo de ejecución"""
        self._estrategia = estrategia

    def calcular_monto(self, tarifa_base, fecha_inicio, fecha_fin, km):
        return self._estrategia.calcular(tarifa_base, fecha_inicio, fecha_fin, km)
```

**Relación:** `CalculadoraTarifa` **TIENE-UN** `TarifaStrategy` (composición, no herencia)

**Ejemplo de uso:**

```python
# Crear calculadora con estrategia simple
calculadora = CalculadoraTarifa(TarifaSimple())
monto1 = calculadora.calcular_monto(5000, fecha1, fecha2)

# Cambiar estrategia en tiempo de ejecución
calculadora.cambiar_estrategia(TarifaPremium())
monto2 = calculadora.calcular_monto(5000, fecha1, fecha2)
```

**Beneficio:** Mayor flexibilidad que herencia, permite cambiar comportamiento dinámicamente.

---

## 6. Patrones de Diseño

### 6.1 Strategy Pattern (Patrón Estrategia)

**Ubicación:** `Backend/app/models/strategies/TarifaStrategy.py`

**Propósito:** Define una familia de algoritmos intercambiables.

**Estructura:**

```
TarifaStrategy (interfaz)
    ├── TarifaSimple
    ├── TarifaConDescuentoSemanal
    ├── TarifaPorKilometraje
    └── TarifaPremium

CalculadoraTarifa (contexto)
    └── usa: TarifaStrategy
```

**Implementación:**

```python
# Estrategia base
class TarifaStrategy(ABC):
    @abstractmethod
    def calcular(self, tarifa_base, fecha_inicio, fecha_fin, km):
        pass

# Estrategias concretas
class TarifaSimple(TarifaStrategy):
    def calcular(self, ...):
        return tarifa_base * dias

class TarifaPremium(TarifaStrategy):
    def calcular(self, ...):
        # Algoritmo diferente
        return (tarifa_base * dias * 0.85) + (km * costo_km)
```

**Ventajas:**
- ✅ Fácil agregar nuevas estrategias sin modificar código existente
- ✅ Cada estrategia en su propia clase (Single Responsibility)
- ✅ Permite cambiar algoritmo en tiempo de ejecución

**Cuándo usar:**
- Cuando tienes múltiples algoritmos para una misma tarea
- Cuando quieres que el cliente elija qué algoritmo usar

---

### 6.2 Factory Pattern (Patrón Fábrica)

**Ubicación:** `Backend/app/models/factories/TarifaFactory.py`

**Propósito:** Centraliza la creación de objetos sin exponer la lógica de creación.

**Implementación:**

```python
class TarifaFactory:
    """Factory para crear estrategias de tarifa"""

    @staticmethod
    def crear_estrategia(tipo_tarifa: str, **kwargs):
        if tipo_tarifa == 'simple':
            return TarifaSimple()
        elif tipo_tarifa == 'semanal':
            return TarifaConDescuentoSemanal()
        elif tipo_tarifa == 'kilometraje':
            return TarifaPorKilometraje(costo_por_km=kwargs.get('costo_por_km', 50))
        elif tipo_tarifa == 'premium':
            return TarifaPremium(costo_por_km=kwargs.get('costo_por_km', 30))
        else:
            raise ValueError(f"Tipo '{tipo_tarifa}' no válido")
```

**Uso:**

```python
# En lugar de hacer:
estrategia = TarifaConDescuentoSemanal()

# Usamos el factory:
estrategia = TarifaFactory.crear_estrategia('semanal')
```

**Ventajas:**
- ✅ Código cliente no conoce las clases concretas
- ✅ Fácil agregar nuevos tipos sin cambiar código cliente
- ✅ Centraliza lógica de creación

---

### 6.3 Repository Pattern (Patrón Repositorio)

**Ubicación:** `Backend/app/repository/`

**Propósito:** Abstrae el acceso a datos, separando lógica de negocio de lógica de persistencia.

**Estructura:**

```
BaseRepository (abstracto)
    ├── VehiculoRepository
    ├── ClienteRepository
    ├── AlquilerRepository
    ├── ReservaRepository
    └── MantenimientoRepository
```

**Beneficios:**
- ✅ Desacopla lógica de negocio de acceso a datos
- ✅ Facilita testing (se puede mockear el repository)
- ✅ Centraliza queries SQL
- ✅ Fácil cambiar de BD (SQLite → PostgreSQL)

---

## 📊 Diagrama de Clases Simplificado

```
┌─────────────────────┐
│   BaseRepository    │ (abstracta)
│   (ABC, Generic)    │
├─────────────────────┤
│ + crear()           │
│ + obtener_todos()   │
│ + obtener_por_id()  │
│ + actualizar()      │
│ + eliminar()        │
└──────────┬──────────┘
           │
    ┌──────┴──────┬──────────────┐
    │             │              │
┌───▼──────┐  ┌──▼────────┐  ┌─▼─────────┐
│ Vehiculo │  │  Cliente  │  │ Alquiler  │
│Repository│  │Repository │  │Repository │
└──────────┘  └───────────┘  └───────────┘


┌─────────────────┐
│   Persona       │ (abstracta)
├─────────────────┤
│ - _nombre       │
│ - _apellido     │
│ + to_dict()     │ (abstracto)
│ + get_tipo()    │ (abstracto)
└────────┬────────┘
         │
    ┌────┴─────┐
    │          │
┌───▼───┐  ┌──▼──────┐
│Cliente│  │Empleado │
└───────┘  └─────────┘


┌──────────────────┐
│ TarifaStrategy   │ (abstracta)
├──────────────────┤
│ + calcular()     │
└────────┬─────────┘
         │
    ┌────┴────┬──────────────┬─────────────┐
    │         │              │             │
┌───▼──┐  ┌──▼──────┐  ┌────▼────┐  ┌────▼─────┐
│Simple│  │Semanal  │  │Kilometraje│ │Premium  │
└──────┘  └─────────┘  └──────────┘  └──────────┘
                            │
                            │
                    ┌───────▼────────┐
                    │ Calculadora    │
                    │   Tarifa       │
                    │ (composición)  │
                    └────────────────┘
```

---

## 🎯 Resumen de Aplicación de Conceptos

| Concepto POO | Archivo Principal | Líneas Clave |
|--------------|------------------|--------------|
| **Herencia** | `BaseRepository.py` | 18-80 |
| **Herencia** | `Persona.py` | 1-130 |
| **Polimorfismo** | `TarifaStrategy.py` | 35-160 |
| **Abstracción** | `BaseRepository.py` | 18 (`ABC`) |
| **Abstracción** | `Persona.py` | 10 (`ABC`) |
| **Encapsulamiento** | `Persona.py` | 25-65 (properties) |
| **Composición** | `TarifaStrategy.py` | 165-195 |
| **Strategy Pattern** | `TarifaStrategy.py` | 1-200 |
| **Factory Pattern** | `TarifaFactory.py` | 1-90 |
| **Repository Pattern** | `BaseRepository.py` | Todo el archivo |

---

## 💡 Ejemplos de Uso en el Sistema

### Ejemplo 1: Usar Strategy Pattern para Calcular Tarifa

```python
from app.models.strategies.TarifaStrategy import CalculadoraTarifa, TarifaPremium
from datetime import datetime

# Crear calculadora con estrategia premium
calculadora = CalculadoraTarifa(TarifaPremium(costo_por_km=30))

# Calcular monto
fecha_inicio = datetime(2025, 1, 15)
fecha_fin = datetime(2025, 1, 25)  # 10 días
tarifa_base = 8000

monto = calculadora.calcular_monto(
    tarifa_base=tarifa_base,
    fecha_inicio=fecha_inicio,
    fecha_fin=fecha_fin,
    km_recorridos=500
)

print(f"Monto total: ${monto}")
# Output: Monto total: $83000.0
# (8000 * 10 * 0.85 + 500 * 30)
```

### Ejemplo 2: Usar Factory para Crear Estrategias

```python
from app.models.factories.TarifaFactory import TarifaFactory

# Crear diferentes estrategias usando el factory
estrategia_simple = TarifaFactory.crear_estrategia('simple')
estrategia_premium = TarifaFactory.crear_estrategia('premium', costo_por_km=25)

# Ver tipos disponibles
print(TarifaFactory.tipos_disponibles())
# ['simple', 'semanal', 'kilometraje', 'premium']
```

### Ejemplo 3: Polimorfismo con Repositorios

```python
from app.repository.VehiculoRepository import VehiculoRepository
from app.repository.ClienteRepository import ClienteRepository

# Ambos repositorios heredan de BaseRepository
# Por lo tanto, tienen la misma interfaz

repos = [VehiculoRepository(), ClienteRepository()]

for repo in repos:
    # Polimorfismo: mismo método, comportamiento diferente
    entidades = repo.obtener_todos()
    print(f"Total de entidades: {len(entidades)}")
```

---

## 📝 Conclusión

Este proyecto demuestra la aplicación práctica de los principales conceptos de POO:

✅ **Herencia** - Reutilización de código a través de clases base
✅ **Polimorfismo** - Mismo método, diferentes implementaciones
✅ **Abstracción** - Clases abstractas que definen contratos
✅ **Encapsulamiento** - Protección de datos con propiedades
✅ **Composición** - Relaciones "tiene-un" flexibles
✅ **Patrones de Diseño** - Strategy, Factory y Repository

Todos estos conceptos trabajan juntos para crear un sistema **mantenible**, **extensible** y **testeable**.

---

**Autor:** Sistema de Gestión de Alquileres
**Materia:** Desarrollo de Aplicaciones con Objetos
**Fecha:** Noviembre 2025
