import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        # Configuración estándar para tu entorno local de MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Si tu MySQL Workbench tiene contraseña, ponla entre las comillas
            database='mundo_mascota'
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
