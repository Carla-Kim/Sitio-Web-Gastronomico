import re
from ..database.categorias import update_categoria, insert_categoria, seleccionar_categorias, delete_categoria
from ..utils.errors import *
from ..utils.pagination import build_links
from ..database.connection import get_connection, get_cursor

def actualizar_categoria(id, data):
    if not data or 'nombre' not in data:
        return 'body_invalido'

    nombre = data["nombre"]

    if re.fullmatch(r'[A-Za-z0-9 áéíóúÁÉÍÓÚñÑüÜ]+', nombre) is None or len(nombre) > 100:
        return 'nombre_invalido'

    try:
        rows = update_categoria(id, nombre)
    except Exception:
        return 'error_db'

    if rows == 0:
        return 'categoria_no_encontrada'
    
    return 'exito'


def crear_categoria(data):
    if not data or 'nombre' not in data:
        return 'body_invalido'

    nombre = data["nombre"]

    if re.fullmatch(r'[A-Za-z0-9 áéíóúÁÉÍÓÚñÑüÜ]+', nombre) is None or len(nombre) > 100:
        return 'nombre_invalido' 

    try:
        resultado = insert_categoria(nombre)
        if resultado == 'duplicado':
            return 'nombre_duplicado'
        return 'exito', resultado  
    except Exception:
        return 'error_db'


def obtener_categorias(base_url, query_params, limit, offset):
    categorias, total = seleccionar_categorias(limit, offset)

    if total == 0:
        raise ValueError("NOT_FOUND")

    args_for_links = query_params.copy()
    args_for_links.pop("_limit", None)
    args_for_links.pop("_offset", None)
    args_for_links.pop("limit", None)
    args_for_links.pop("offset", None)
    links = build_links(base_url, args_for_links, limit, offset, total)

    response_body = {
        "_links": links,
        "count": total,
        "data": categorias
    }
    
    return response_body


def eliminar_categoria(id):
    try:
        rows = delete_categoria(id)
    except Exception:
        return 'error_db'
    if rows == 0:
        return 'no_encontrada'
    return 'exito'