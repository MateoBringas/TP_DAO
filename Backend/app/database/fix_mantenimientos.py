"""
Script para arreglar la tabla de mantenimientos
"""
import sqlite3
import os

def fix_mantenimientos_table():
    db_path = os.path.join(os.path.dirname(__file__), "database.db")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("Arreglando tabla de mantenimientos...")

        # Verificar si existe la tabla
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mantenimientos'")
        if cursor.fetchone():
            print("Respaldando tabla actual...")
            cursor.execute("DROP TABLE IF EXISTS mantenimientos_backup")
            cursor.execute("CREATE TABLE mantenimientos_backup AS SELECT * FROM mantenimientos")

            print("Eliminando tabla actual...")
            cursor.execute("DROP TABLE mantenimientos")

        # Crear tabla con estructura correcta (sin FK de estado, usando TEXT)
        print("Creando tabla con estructura correcta...")
        cursor.execute("""
            CREATE TABLE mantenimientos (
                id_mantenimiento INTEGER PRIMARY KEY AUTOINCREMENT,
                vehiculo_id INTEGER NOT NULL,
                empleado_id INTEGER NULL,
                estado_mantenimiento TEXT NOT NULL,
                fecha_programada DATE NOT NULL,
                fecha_realizada DATE NULL,
                km INTEGER NULL,
                costo REAL NULL,
                observacion TEXT NULL,
                FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id_vehiculo),
                FOREIGN KEY (empleado_id) REFERENCES empleados(id_empleado)
            )
        """)

        conn.commit()
        print("✓ Tabla mantenimientos arreglada exitosamente")

    except sqlite3.Error as e:
        print(f"✗ Error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    fix_mantenimientos_table()
