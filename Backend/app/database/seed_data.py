import sqlite3
import os
from datetime import datetime, timedelta

try:
    db_path = os.path.join(os.path.dirname(__file__), "database.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insertar estados de alquiler
    cursor.executemany("""
        INSERT OR IGNORE INTO estados_alquiler (codigo) VALUES (?)
    """, [
        ('PENDIENTE',),
        ('ACTIVO',),
        ('FINALIZADO',),
        ('CANCELADO',)
    ])

    # Insertar estados de reserva
    cursor.executemany("""
        INSERT OR IGNORE INTO estados_reserva (codigo) VALUES (?)
    """, [
        ('PENDIENTE',),
        ('CONFIRMADA',),
        ('CANCELADA',),
        ('COMPLETADA',)
    ])

    # Insertar estados de mantenimiento
    cursor.executemany("""
        INSERT OR IGNORE INTO estados_mantenimiento (codigo) VALUES (?)
    """, [
        ('PROGRAMADO',),
        ('EN_PROCESO',),
        ('COMPLETADO',),
        ('CANCELADO',)
    ])

    # Insertar estados de incidente
    cursor.executemany("""
        INSERT OR IGNORE INTO estados_incidente (codigo) VALUES (?)
    """, [
        ('REPORTADO',),
        ('EN_REVISION',),
        ('RESUELTO',),
        ('CERRADO',)
    ])

    # Insertar tipos de incidente
    cursor.executemany("""
        INSERT OR IGNORE INTO tipos_incidente (codigo, cubre_seguro) VALUES (?, ?)
    """, [
        ('ACCIDENTE', 1),
        ('ROBO', 1),
        ('DANO_MENOR', 0),
        ('MULTA', 0),
        ('AVERIA_MECANICA', 0)
    ])

    # Insertar empleados de ejemplo
    cursor.executemany("""
        INSERT OR IGNORE INTO empleados (nombre, apellido, dni, email, telefono, habilitado)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        ('Juan', 'Pérez', '12345678', 'juan.perez@empresa.com', '1122334455', 1),
        ('María', 'González', '87654321', 'maria.gonzalez@empresa.com', '1155667788', 1),
        ('Carlos', 'Rodríguez', '11223344', 'carlos.rodriguez@empresa.com', '1133445566', 1)
    ])

    # Insertar clientes de ejemplo
    cursor.executemany("""
        INSERT OR IGNORE INTO clientes (dni, nombre, apellido, email, telefono, direccion, licencia_num, licencia_venc, habilitado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        ('20111222', 'Pedro', 'Martínez', 'pedro.martinez@email.com', '1144556677',
         'Av. Corrientes 1234', 'LIC001', '2026-12-31', 1),
        ('30222333', 'Ana', 'López', 'ana.lopez@email.com', '1166778899',
         'Calle Falsa 123', 'LIC002', '2025-06-30', 1),
        ('40333444', 'Luis', 'Fernández', 'luis.fernandez@email.com', '1177889900',
         'Av. Libertador 5678', 'LIC003', '2027-03-15', 1)
    ])

    # Insertar vehículos de ejemplo
    vehiculos_ejemplo = [
        ('ABC123', 'Toyota', 'Corolla', 2022, 8000.00, 15000, '2025-12-31', '2025-06-30', 10000, 10000, '2024-01-15', 1),
        ('DEF456', 'Ford', 'Focus', 2021, 7500.00, 25000, '2025-10-31', '2025-08-31', 10000, 20000, '2024-05-20', 1),
        ('GHI789', 'Chevrolet', 'Cruze', 2023, 9000.00, 8000, '2026-01-31', '2025-12-31', 10000, 0, '2024-01-01', 1),
        ('JKL012', 'Volkswagen', 'Vento', 2022, 8500.00, 18000, '2025-11-30', '2025-07-31', 10000, 10000, '2024-03-10', 1),
        ('MNO345', 'Honda', 'Civic', 2023, 9500.00, 12000, '2026-02-28', '2026-01-31', 10000, 10000, '2024-06-01', 1),
        ('PQR678', 'Renault', 'Logan', 2020, 6500.00, 45000, '2025-09-30', '2025-05-31', 10000, 40000, '2024-02-15', 1),
        ('STU901', 'Peugeot', '208', 2021, 7000.00, 30000, '2025-08-31', '2025-04-30', 10000, 30000, '2024-04-01', 1),
        ('VWX234', 'Fiat', 'Cronos', 2022, 7200.00, 20000, '2025-10-15', '2025-06-15', 10000, 20000, '2024-05-15', 1)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO vehiculos
        (patente, marca, modelo, anio, tarifa_base_dia, km_actual, seguro_venc, vtv_venc,
         km_service_cada, km_ultimo_service, fecha_ultimo_service, habilitado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, vehiculos_ejemplo)

    conn.commit()
    print(f"Datos de ejemplo insertados correctamente")
    print(f"  - {len(vehiculos_ejemplo)} vehiculos")
    print(f"  - 3 empleados")
    print(f"  - 3 clientes")
    print(f"  - Estados y tipos de incidente inicializados")

except sqlite3.Error as e:
    print(f"Error al insertar datos: {e}")

finally:
    if conn:
        conn.close()
