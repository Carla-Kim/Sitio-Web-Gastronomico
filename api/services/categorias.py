import re
from ..database.categorias import *

def actualizar_categoria(id, data):
    if not data or 'nombre' not in data:
        return 'body_invalido'

    nombre = data["nombre"]

    if re.fullmatch(r'[A-Za-z0-9 ]+', nombre) is None or len(nombre) > 100:
        return 'nombre_invalido'

    try:
        rows = update_categoria(id, nombre)
    
    except Exception:
        return 'error_db'

    if not rows:
        return 'categoria_no_encontrada'
    
    return 'exito'
