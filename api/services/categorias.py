import re
from ..database.categorias import *


#Función para el endpoint update categoría
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


#Función para el endpoint de agregar categoría
def crear_categoria(data):
    if not data or 'nombre' not in data:
        return 'body_invalido'

    nombre = data["nombre"]

    if re.fullmatch(r'[A-Za-z0-9 ]+', nombre) is None or len(nombre) > 100:
        return 'nombre_invalido' 

    try:
        resultado = insert_categoria(nombre)
        if resultado == 'duplicado':
            return 'nombre_duplicado'
        return 'exito', resultado  
    except Exception:
        return 'error_db'
