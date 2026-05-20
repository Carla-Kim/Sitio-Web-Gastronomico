import mysql.connector
from config import DB_CONFIG, DB_NAME

# Conexión a la base de datos; a delegar en /database/connection.py
# def get_connection():
#    return mysql.connector.connect(**DB_CONFIG, database=DB_NAME)

#Update categoría
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
        count_query = "SELECT COUNT(*) AS total FROM Categorias"
        cursor.execute(count_query)
        total = cursor.fetchone()['total']

        query = "SELECT * FROM Categorias ORDER BY categorias_id LIMIT %s OFFSET %s"
        cursor.execute(query, [limit, offset])
        categorias = cursor.fetchall()

        return categorias, total

    finally:
        cursor.close()
        conn.close()
