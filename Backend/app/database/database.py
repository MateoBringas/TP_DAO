import sqlite3
from contextlib import contextmanager
import os

# Ruta de la base de datos (dentro de la carpeta database)
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

@contextmanager
def get_connection():
    """Devuelve una conexión SQLite lista para usar"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acceder por nombre de columna
    try:
        yield conn
    finally:
        conn.close()
