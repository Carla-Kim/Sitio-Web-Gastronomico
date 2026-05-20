import mysql.connector
from config import DB_CONFIG, DB_NAME

# Conexión a la base de datos; a delegar en /database/connection.py
def get_connection():
    return mysql.connector.connect(**DB_CONFIG, database=DB_NAME)

def update_categoria(id, nombre):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE categorias SET nombre = %s WHERE categoria_id = %s",
            (nombre, id)
        )
        conn.commit()
        return cursor.rowcount

    except Exception as err:
        conn.rollback()
        raise err

    finally:
        cursor.close()
        conn.close()
