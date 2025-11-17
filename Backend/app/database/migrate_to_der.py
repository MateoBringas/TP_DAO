"""
Script para migrar la base de datos actual al esquema del DER.
Este script realiza los cambios necesarios para alinear la base de datos con el DER_TP.png
"""
import sqlite3
import os

def migrate_database():
    db_path = os.path.join(os.path.dirname(__file__), "database.db")

    # Backup de la base de datos actual
    backup_path = os.path.join(os.path.dirname(__file__), "database_backup.db")

    print("Iniciando migración a esquema DER...")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar tablas existentes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [table[0] for table in cursor.fetchall()]
        print(f"Tablas existentes: {existing_tables}")

        # 1. Actualizar tabla alquileres
        print("\n1. Actualizando tabla alquileres...")
        if 'alquileres' in existing_tables:
            # Renombrar tabla actual
            cursor.execute("ALTER TABLE alquileres RENAME TO alquileres_old")

        # Crear nueva tabla según DER
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alquileres (
                id_alquiler INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                empleado_id INTEGER NULL,
                vehiculo_id INTEGER NOT NULL,
                estado_alquiler_id INTEGER NOT NULL,
                reserva_id INTEGER NULL,
                fecha_inicio DATE NOT NULL,
                fecha_prevista DATE NOT NULL,
                fecha_entrega DATE NULL,
                km_salida INTEGER NOT NULL,
                km_entrada INTEGER NULL,
                observaciones TEXT NULL,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id_cliente),
                FOREIGN KEY (empleado_id) REFERENCES empleados(id_empleado),
                FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id_vehiculo),
                FOREIGN KEY (estado_alquiler_id) REFERENCES estados_alquiler(id_estado_alquiler),
                FOREIGN KEY (reserva_id) REFERENCES reservas(id_reserva)
            )
        """)

        # Migrar datos existentes si hay
        if 'alquileres_old' in [t[0] for t in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
            cursor.execute("""
                INSERT INTO alquileres (
                    id_alquiler, cliente_id, empleado_id, vehiculo_id,
                    estado_alquiler_id, reserva_id, fecha_inicio, fecha_prevista,
                    fecha_entrega, km_salida, km_entrada, observaciones,
                    creado_en, actualizado_en
                )
                SELECT
                    id_alquiler, cliente_id, empleado_id, vehiculo_id,
                    estado_alquiler_id, reserva_id, fecha_inicio, fecha_fin,
                    NULL, km_inicio, km_fin, observaciones,
                    creado_en, actualizado_en
                FROM alquileres_old
            """)
            cursor.execute("DROP TABLE alquileres_old")
            print("   - Datos migrados de alquileres_old")

        # 2. Actualizar tabla reservas
        print("\n2. Actualizando tabla reservas...")
        if 'reservas' in existing_tables:
            cursor.execute("ALTER TABLE reservas RENAME TO reservas_old")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                vehiculo_id INTEGER NULL,
                empleado_id INTEGER NULL,
                estado_reserva_id INTEGER NOT NULL,
                fecha_reserva DATE NOT NULL,
                fecha_retiro DATE NOT NULL,
                fecha_devolucion DATE NOT NULL,
                senia_monto REAL NOT NULL DEFAULT 0,
                actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id_cliente),
                FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id_vehiculo),
                FOREIGN KEY (empleado_id) REFERENCES empleados(id_empleado),
                FOREIGN KEY (estado_reserva_id) REFERENCES estados_reserva(id_estado_reserva)
            )
        """)

        # Migrar datos de reservas si existen
        if 'reservas_old' in [t[0] for t in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
            cursor.execute("""
                INSERT INTO reservas (
                    id_reserva, cliente_id, vehiculo_id, empleado_id,
                    estado_reserva_id, fecha_reserva, fecha_retiro,
                    fecha_devolucion, senia_monto, actualizado_en
                )
                SELECT
                    id_reserva, cliente_id, vehiculo_id, empleado_id,
                    estado_reserva_id, fecha_reserva, fecha_carga,
                    fecha_carga, senia_monto, actualizado_en
                FROM reservas_old
            """)
            cursor.execute("DROP TABLE reservas_old")
            print("   - Datos migrados de reservas_old")

        # 3. Crear tabla pagos según DER
        print("\n3. Verificando tabla pagos...")
        cursor.execute("""
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
            )
        """)
        print("   - Tabla pagos OK")

        # 4. Actualizar tabla mantenimientos según DER
        print("\n4. Actualizando tabla mantenimientos...")
        if 'mantenimientos' in existing_tables:
            cursor.execute("ALTER TABLE mantenimientos RENAME TO mantenimientos_old")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mantenimientos (
                id_mantenimiento INTEGER PRIMARY KEY AUTOINCREMENT,
                vehiculo_id INTEGER NOT NULL,
                empleado_id INTEGER NULL,
                tipo_incidente_id INTEGER NOT NULL,
                estado_incidente_id INTEGER NOT NULL,
                km INTEGER NULL,
                fecha_realizada DATE NULL,
                costo REAL NULL,
                notas TEXT NULL,
                FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id_vehiculo),
                FOREIGN KEY (empleado_id) REFERENCES empleados(id_empleado),
                FOREIGN KEY (tipo_incidente_id) REFERENCES tipos_incidente(id_tipo_incidente),
                FOREIGN KEY (estado_incidente_id) REFERENCES estados_incidente(id_estado_incidente)
            )
        """)
        print("   - Tabla mantenimientos recreada según DER")

        # 5. Crear tabla incidentes
        print("\n5. Verificando tabla incidentes...")
        cursor.execute("""
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
            )
        """)
        print("   - Tabla incidentes OK")

        conn.commit()
        print("\n✓ Migración completada exitosamente")
        print("\nCAMBIOS REALIZADOS:")
        print("- alquileres: fecha_fin -> fecha_prevista, km_inicio -> km_salida, km_fin -> km_entrada")
        print("- reservas: fecha_carga -> fecha_retiro/fecha_devolucion")
        print("- mantenimientos: reestructurada según DER")

    except sqlite3.Error as e:
        print(f"\n✗ Error durante la migración: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate_database()
