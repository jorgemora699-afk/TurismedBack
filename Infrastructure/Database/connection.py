"""
Database Connection
===================

Maneja la conexión a PostgreSQL.

Responsabilidad:
- Crear conexiones a la base de datos
- Cerrar conexiones correctamente
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG


def get_db_connection():
    """
    Crea y retorna una conexión a PostgreSQL

    Returns:
        connection: Objeto de conexión a PostgreSQL
        None: Si falla la conexión
    """
    try:
        connection = psycopg2.connect(
            host=DB_CONFIG['host'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port'],
            cursor_factory=RealDictCursor  # Los resultados vienen como dict
        )
        return connection
    except Exception as error:
        print(f"Error connecting to database: {str(error)}")
        return None


def close_db_connection(connection, cursor=None):
    """
    Cierra la conexión a la base de datos

    Args:
        connection: Conexión a cerrar
        cursor: Cursor a cerrar (opcional)
    """
    if cursor:
        cursor.close()
    if connection:
        connection.close()
