import os
import mysql.connector
from api.database.config import DB_NAME, DB_CONFIG

def get_connection():
    return mysql.connector.connect(
        database=DB_NAME,
        **DB_CONFIG
    )

def get_cursor():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error en la consulta (Se hizo Rollback): {e}") # chequear si entra en errors.py o no
        raise e
    finally:
        cursor.close()
        conn.close()
