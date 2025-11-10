# Backend - Proyecto de Alquiler de Vehículos

Proyecto backend en Flask que gestiona vehículos, clientes, reservas, alquileres, pagos, mantenimientos e incidentes.

Estructura del proyecto:
- app/
  - __init__.py          (crea la app y registra blueprints)
  - main.py              (entrada de la aplicación)
  - database/
    - database.db        (archivo SQLite generado)
    - database.py        (helper de conexión)
    - init_db.py         (script para inicializar esquemas)
  - models/              (Modelos)
    - Vehiculo.py
    - Cliente.py
    - Empleado.py
    - Alquiler.py
    - Reserva.py
    - Pago.py
    - Mantenimiento.py
    - Incidente.py
  - repository/          (Consultas a BD)
    - VehiculoRepository.py
  - services/            (Logica de la app)
    - VehiculoService.py
  - routes/              (Ruter de la app)
    - Vehiculo.py

Requisitos
- Python >= 3.10
- Dependencias listadas en [requirements.txt](requirements.txt)

Instalación rápida
1. Crear y activar entorno virtual
   - macOS / Linux
     python3 -m venv venv
     source venv/bin/activate
   - Windows
     python -m venv venv
     venv\Scripts\activate

2. Instalar dependencias
   pip install -r requirements.txt

Base de datos
- El archivo SQLite se crea en: app/database/database.db
- Para crear las tablas iniciales ejecutar:
  python3 app/database/init_db.py

Ejecución
- Ejecutar la aplicación Flask:
  python3 -m app.main