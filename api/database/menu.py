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
def check_by_id(cursor, id):
    cursor.execute("SELECT 1 FROM productos WHERE id_producto = %s", (id,))
    return cursor.fetchone() is not None

def editar_producto(cursor, id, categoria, nombre, precio):
    query = 'UPDATE productos SET categorias_id = %s, nombre = %s, precio = %s WHERE id_producto = %s'
    cursor.execute(query,(categoria, nombre, precio, id))

def obtener_productos(cursor, limit, offset):
    sql_count = "SELECT COUNT(*) as count FROM productos"
    sql_elems = "SELECT product_id, categorias_id, nombre, precio FROM productos LIMIT %s OFFSET %s"

    cursor.execute(sql_count)
    count = cursor.fetchone()["count"]

    cursor.execute(sql_elems, (limit, offset))  #limit y offset para la paginacion
    rows = cursor.fetchall()

    return {
        "rows": rows,
        "count": count
    }

def check_by_nombre(cursor, nombre):
    query = "SELECT 1 FROM Productos WHERE nombre = %s"
    cursor.execute(query, (nombre,))
    return cursor.fetchone() is not None

def ingresar_producto(cursor, categoria_id, nombre, precio):
    query = """
        INSERT INTO Productos (categorias_id, nombre, precio) 
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (categoria_id, nombre, precio))
    return cursor.lastrowid