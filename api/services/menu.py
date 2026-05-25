from api.database import menu as menu_db
from api.utils.errors import ReturnErrors
from api.utils.pagination import build_links
from api.database.connection import get_connection, get_cursor

def ingresar_producto(data):
    if not data:
        return ReturnErrors(400), 400
        
    categoria_id = data.get('categoria_id')
    nombre = data.get('nombre')
    precio = data.get('precio')
    
    if not all([categoria_id, nombre, precio]):
        return ReturnErrors(400), 400
        
    try:
        with get_cursor() as cursor:
            
            if menu_db.check_by_nombre(cursor, nombre):
                return ReturnErrors(409), 409
                
            nuevo_id = menu_db.ingresar_producto(cursor, categoria_id, nombre, precio)
            
            resultado = {
                "status": "success",
                "message": "Producto ingresado correctamente.",
                "producto_id": nuevo_id
            }
            return resultado, 201

    except Exception as e:
        return ReturnErrors(500), 500

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


#codigo: consultar productos
def ver_productos(base_url,query_params, limit, offset):
    productos, total = menu_db.obtener_productos(limit, offset)

    if total == 0:
        raise ValueError("NOT_FOUND")

    args_for_links = query_params.copy()
    args_for_links.pop("_limit", None)
    args_for_links.pop("_offset", None)

    links = build_links(base_url, args_for_links, limit, offset, total)

    response_body = {
        "_links": links,
        "count": total,
        "data": productos
    }
    
    return response_body
    


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
