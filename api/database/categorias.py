import mysql.connector
from .config import DB_CONFIG, DB_NAME
from .connection import get_connection

#Update categoría
def update_categoria(id, nombre):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Categorias SET nombre = %s WHERE categorias_id = %s",
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

#Insert categoría
def insert_categoria(nombre):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Categorias (nombre) VALUES (%s)",
            (nombre,)
        )
        conn.commit()
        return cursor.lastrowid
    
    except mysql.connector.Error as err:
        conn.rollback()
        if err.errno == 1062:
            return 'duplicado'
        raise err
    
    except Exception as err:
        conn.rollback()
        raise err
    
    finally:
        cursor.close()
        conn.close()
    
# listado de categorías
def seleccionar_categorias(limit, offset):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT categorias_id, nombre 
            FROM Categorias 
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (limit, offset))
        categorias = cursor.fetchall()
        
        cursor.execute("SELECT COUNT(*) AS total FROM Categorias")
        total = cursor.fetchone()["total"]

        return categorias, total

    finally:
        cursor.close()
        conn.close()