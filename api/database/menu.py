import mysql.connector
from config import DB_CONFIG, DB_NAME

def get_connection():
    return mysql.connector.connect(**DB_CONFIG, database=DB_NAME)

def borrar_producto(id_producto):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM productos WHERE producto_id = %s",(id_producto,)
        )
        conn.commit()
        return cursor.rowcount
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        cursor.close()
        conn.close()
