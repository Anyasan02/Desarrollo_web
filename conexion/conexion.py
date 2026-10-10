import os
import psycopg2
from psycopg2.extras import RealDictCursor


def obtener_conexion():
    try:
        url_base_datos = os.environ.get("DATABASE_URL")

        if not url_base_datos:
            raise Exception("No se encontró DATABASE_URL")

        conexion = psycopg2.connect(
            url_base_datos,
            cursor_factory=RealDictCursor
        )

        return conexion

    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None