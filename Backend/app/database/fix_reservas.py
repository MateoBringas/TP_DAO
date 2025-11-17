"""
Script para arreglar la tabla de reservas
"""
import sqlite3
import os

def fix_reservas_table():
    db_path = os.path.join(os.path.dirname(__file__), "database.db")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("Arreglando tabla de reservas...")

        # Verificar si existe la tabla
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reservas'")
        if cursor.fetchone():
            print("Respaldando datos actuales...")
            cursor.execute("DROP TABLE IF EXISTS reservas_backup")
            cursor.execute("CREATE TABLE reservas_backup AS SELECT * FROM reservas")

            # Obtener datos existentes
            cursor.execute("SELECT * FROM reservas_backup")
            reservas_existentes = cursor.fetchall()

            print("Eliminando tabla actual...")
            cursor.execute("DROP TABLE reservas")

        # Crear tabla con estructura correcta
        print("Creando tabla con estructura correcta...")
        cursor.execute("""
            CREATE TABLE reservas (
                id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                vehiculo_id INTEGER NULL,
                empleado_id INTEGER NULL,
                estado_reserva_id INTEGER NOT NULL,
                fecha_reserva DATE NOT NULL,
                fecha_alquiler DATE NOT NULL,
                senia_monto REAL NOT NULL DEFAULT 0,
                actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id_cliente),
                FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id_vehiculo),
                FOREIGN KEY (empleado_id) REFERENCES empleados(id_empleado),
                FOREIGN KEY (estado_reserva_id) REFERENCES estados_reserva(id_estado_reserva)
            )
        """)

        # Restaurar datos si existían
        if 'reservas_existentes' in locals() and reservas_existentes:
            print(f"Restaurando {len(reservas_existentes)} reservas...")
            cursor.execute("SELECT * FROM reservas_backup LIMIT 1")
            columnas = [desc[0] for desc in cursor.description]

            # Mapear columnas viejas a nuevas
            for fila_dict in reservas_existentes:
                # Convertir Row a dict usando los nombres de columnas
                fila = dict(zip(columnas, fila_dict))

                cursor.execute("""
                    INSERT INTO reservas (
                        id_reserva, cliente_id, vehiculo_id, empleado_id,
                        estado_reserva_id, fecha_reserva, fecha_alquiler,
                        senia_monto, actualizado_en
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    fila.get('id_reserva'),
                    fila.get('cliente_id'),
                    fila.get('vehiculo_id'),
                    fila.get('empleado_id'),
                    fila.get('estado_reserva_id'),
                    fila.get('fecha_reserva'),
                    fila.get('fecha_carga') or fila.get('fecha_alquiler'),  # usar fecha_carga si existe
                    fila.get('senia_monto', 0),
                    fila.get('actualizado_en')
                ))

        conn.commit()
        print("✓ Tabla reservas arreglada exitosamente")

    except sqlite3.Error as e:
        print(f"✗ Error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    fix_reservas_table()
