import os
import psycopg2
from psycopg2.extras import RealDictCursor

def obtener_conexion():
    try:
        # Render le dará a la app esta variable automáticamente en internet
        url_base_datos = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/mundo_mascota')
        conexion = psycopg2.connect(url_base_datos, cursor_factory=RealDictCursor)
        return conexion
    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None
