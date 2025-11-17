"""
Script para agregar campo foto_url a la tabla vehiculos
"""
import sqlite3
import os

def add_foto_field():
    db_path = os.path.join(os.path.dirname(__file__), "database.db")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("Agregando campo foto_url a tabla vehiculos...")

        # Verificar si el campo ya existe
        cursor.execute("PRAGMA table_info(vehiculos)")
        columnas = [col[1] for col in cursor.fetchall()]

        if 'foto_url' in columnas:
            print("El campo foto_url ya existe en la tabla vehiculos")
            return

        # Agregar el nuevo campo
        cursor.execute("""
            ALTER TABLE vehiculos
            ADD COLUMN foto_url TEXT DEFAULT NULL
        """)

        conn.commit()
        print("Campo foto_url agregado exitosamente")

    except sqlite3.Error as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    add_foto_field()
