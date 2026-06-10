from .connection import get_connection

def borrar_producto(id_producto):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM Productos WHERE producto_id = %s", (id_producto,)
        )
        conn.commit()
        return cursor.rowcount
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        cursor.close()
        conn.close()

def check_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM Productos WHERE producto_id = %s", (id,))
        return cursor.fetchone() is not None
    except Exception as err:
        raise err
    finally:
        cursor.close()
        conn.close()

def editar_producto(id, categoria, nombre, descripcion, precio):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "UPDATE Productos SET categorias_id = %s, nombre = %s, descripcion = %s, precio = %s WHERE producto_id = %s"
        cursor.execute(query, (categoria, nombre, descripcion, precio, id))
        conn.commit()
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        cursor.close()
        conn.close()

def obtener_productos(limit, offset, filtro, direccion_filtro):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        sql_count = "SELECT COUNT(*) as count FROM Productos"
        sql_elems = f"SELECT producto_id, categorias_id, nombre, descripcion, precio FROM Productos ORDER BY {filtro} {direccion_filtro} LIMIT %s OFFSET %s"

        cursor.execute(sql_count)
        res_count = cursor.fetchone()
        #
        # count = res_count["count"] if isinstance(res_count, dict) else res_count[0]
        # error si devuelve un numero, no se puede acceder a count
        if isinstance(res_count, dict):
            count = res_count["count"]
        elif isinstance(res_count, (tuple, list)):
            count = res_count[0]
        else:
            count = res_count

        cursor.execute(sql_elems, (limit, offset))
        rows = cursor.fetchall()

        return {
            "rows": rows,
            "count": count
        }
    except Exception as err:
        raise err
    finally:
        cursor.close()
        conn.close()

def check_by_nombre(nombre):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT 1 FROM Productos WHERE nombre = %s"
        cursor.execute(query, (nombre,))
        return cursor.fetchone() is not None
    except Exception as err:
        raise err
    finally:
        cursor.close()
        conn.close()

def obtener_producto_por_nombre(nombre):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT producto_id, nombre, precio, descripcion FROM Productos WHERE nombre = %s"
        cursor.execute(query, (nombre,))
        return cursor.fetchone() 
    except Exception as err:
        raise err
    finally:
        cursor.close()
        conn.close()

def ingresar_producto(categoria_id, nombre,descripcion ,precio):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO Productos (categorias_id, nombre, descripcion, precio) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (categoria_id, nombre, descripcion, precio))
        conn.commit()
        return cursor.lastrowid
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        cursor.close()
        conn.close()
