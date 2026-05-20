from api.database import menu as menu_db
from data import get_cursor
from api.utils.errors import ReturnErrors

def editar_producto(id, data):
    if not data:
        return ReturnErrors(400), 400
    categoria_id = data.get('categoria_id')
    nombre = data.get('nombre')
    precio = data.get('precio')
    
    if not all([categoria_id, nombre, precio]):
        return ReturnErrors(400),400
    
    try:
        with get_cursor() as cursor:
            exists_id = menu_db.check_by_id(cursor, id)
            if not exists_id:
                return ReturnErrors(404), 404
            
            menu_db.editar_producto(cursor, id, categoria_id, nombre, precio)

    except Exception:
        return ReturnErrors(500), 500
    
    return "", 204


#codifo: consultar productos
def ver_productos(base_url, limit, offset):
    # schema_errors = validate_schema(
    #    PaginationSchema,
    #    limit=limit,
    #    offset=offset
    #)
    #if schema_errors:
    #   return ReturnErrors(400), 400   parte de la paginacion
    try:
        with get_cursor() as cursor:
            productos = menu_db.obtener_productos(cursor, limit, offset)
    except Exception:
        return ReturnErrors(500), 500
    
    productos = [{
        "id": d["producto_id"],
        "categoria": d["categorias_id"],
        "nombre": d["nombre"],
        "precio": d["precio"]
    } for d in productos["rows"] ]

    count = productos["count"]

    return {
        "usuarios": usuarios,
        #"_links": build_links(base_url, {}, limit, offset, count)  de la paginacion
    }, 200
