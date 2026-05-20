def elimina_producto(id_producto):
    if id_producto is None:
        return 'id_invalido'
    
    try:
        resultado = borrar_producto(id_producto)
    except Exception:
        return 'Error_db'
    
    if resultado == 0:
        return 'Producto_no_encontrado'
    
    return 'Se elimino correctamente'
