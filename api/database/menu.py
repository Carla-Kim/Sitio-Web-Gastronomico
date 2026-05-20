def check_by_id(cursor, id):
    cursor.execute("SELECT 1 FROM productos WHERE id_producto = %s", (id,))
    return cursor.fetchone() is not None

def editar_producto(cursor, id, categoria, nombre, precio):
    query = 'UPDATE productos SET categorias_id = %s, nombre = %s, precio = %s WHERE id_producto = %s'
    cursor.execute(query,(categoria, nombre, precio, id))