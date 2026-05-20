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