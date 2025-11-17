import sqlite3
import os

try:
    # Crear conexión dentro de la carpeta actual
    db_path = os.path.join(os.path.dirname(__file__), "database.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS estados_alquiler (
        id_estado_alquiler INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS estados_reserva (
        id_estado_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS estados_mantenimiento (
        id_estado_mantenimiento INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS estados_incidente (
        id_estado_incidente INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS tipos_incidente (
        id_tipo_incidente INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL UNIQUE,
        cubre_seguro BOOLEAN NOT NULL DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS clientes (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        dni TEXT NULL,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        telefono TEXT NOT NULL,
        direccion TEXT NULL,
        licencia_num TEXT NOT NULL UNIQUE,
        licencia_venc DATE NOT NULL,
        habilitado BOOLEAN NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS empleados (
        id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        dni TEXT NULL,
        email TEXT NOT NULL UNIQUE,
        telefono TEXT NULL,
        habilitado BOOLEAN NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS vehiculos (
        id_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
        patente TEXT NOT NULL UNIQUE,
        marca TEXT NOT NULL,
        modelo TEXT NOT NULL,
        anio INTEGER NOT NULL,
        tarifa_base_dia REAL NOT NULL,
        km_actual INTEGER NOT NULL DEFAULT 0,
        seguro_venc DATE NULL,
        vtv_venc DATE NULL,
        km_service_cada INTEGER NULL,
        km_ultimo_service INTEGER NULL,
        fecha_ultimo_service DATE NULL,
        habilitado BOOLEAN NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS mantenimientos (
        id_mantenimiento INTEGER PRIMARY KEY AUTOINCREMENT,
        vehiculo_id INTEGER NOT NULL,
        empleado_id INTEGER NULL,
        estado_mantenimiento_id INTEGER NOT NULL,
        fecha_programada DATE NOT NULL,
        fecha_realizada DATE NULL,
        km INTEGER NULL,
        costo REAL NULL,
        observacion TEXT NULL,
        FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id_vehiculo),
        FOREIGN KEY (estado_mantenimiento_id) REFERENCES estados_mantenimiento(id_estado_mantenimiento),
        FOREIGN KEY (empleado_id) REFERENCES empleados(id_empleado)
    );

    CREATE TABLE IF NOT EXISTS alquileres (
        id_alquiler INTEGER PRIMARY KEY AUTOINCREMENT,
        vehiculo_id INTEGER NOT NULL,
        cliente_id INTEGER NOT NULL,
        empleado_id INTEGER NULL,
        estado_alquiler_id INTEGER NOT NULL,
        reserva_id INTEGER NULL,
        fecha_inicio DATE NOT NULL,
        fecha_fin DATE NOT NULL,
        km_inicio INTEGER NOT NULL,
        km_fin INTEGER NULL,
        monto_total REAL NOT NULL DEFAULT 0,
        observaciones TEXT NULL,
        creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id_vehiculo),
        FOREIGN KEY (cliente_id) REFERENCES clientes(id_cliente),
        FOREIGN KEY (empleado_id) REFERENCES empleados(id_empleado),
        FOREIGN KEY (reserva_id) REFERENCES reservas(id_reserva),
        FOREIGN KEY (estado_alquiler_id) REFERENCES estados_alquiler(id_estado_alquiler)
    );

    CREATE TABLE IF NOT EXISTS pagos (
        id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
        alquiler_id INTEGER NOT NULL,
        empleado_id INTEGER NULL,
        fecha DATETIME NOT NULL,
        monto REAL NOT NULL,
        metodo TEXT NOT NULL,
        descripcion TEXT NULL,
        actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (alquiler_id) REFERENCES alquileres(id_alquiler),
        FOREIGN KEY (empleado_id) REFERENCES empleados(id_empleado)
    );

    CREATE TABLE IF NOT EXISTS reservas (
        id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        vehiculo_id INTEGER NULL,
        empleado_id INTEGER NULL,
        estado_reserva_id INTEGER NOT NULL,
        fecha_reserva DATE NOT NULL,
        fecha_carga DATE NOT NULL,
        senia_monto REAL NOT NULL DEFAULT 0,
        actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id_cliente),
        FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id_vehiculo),
        FOREIGN KEY (empleado_id) REFERENCES empleados(id_empleado),
        FOREIGN KEY (estado_reserva_id) REFERENCES estados_reserva(id_estado_reserva)
    );

    CREATE TABLE IF NOT EXISTS incidentes (
        id_incidente INTEGER PRIMARY KEY AUTOINCREMENT,
        alquiler_id INTEGER NOT NULL,
        tipo_incidente_id INTEGER NOT NULL,
        estado_incidente_id INTEGER NOT NULL,
        empleado_id INTEGER NULL,
        fecha DATETIME NOT NULL,
        descripcion TEXT NULL,
        costo REAL NULL,
        FOREIGN KEY (alquiler_id) REFERENCES alquileres(id_alquiler),
        FOREIGN KEY (tipo_incidente_id) REFERENCES tipos_incidente(id_tipo_incidente),
        FOREIGN KEY (estado_incidente_id) REFERENCES estados_incidente(id_estado_incidente),
        FOREIGN KEY (empleado_id) REFERENCES empleados(id_empleado)
    );
    """)

    conn.commit()
    print(f"Base creada en {db_path}")

except sqlite3.Error as e:
    print(f"Error al crear tablas: {e}")

finally:
    if conn:
        conn.close()
