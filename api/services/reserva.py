import re
from ..database.reservas import *
from ..utils.pagination import build_links

def crear_reserva(data):
    campos = ["fecha", "email", "nombre", "apellido", "DNI", "servicio_ID", "telefono", "cantidad_personas"]
    if not data or not all(i in data for i in campos):
        return 'body_invalido'
    
    fecha = data["fecha"]
    email = data["email"]
    nombre = data["nombre"]
    apellido = data["apellido"]
    dni = data["DNI"]
    servicio_id = data["servicio_ID"]
    telefono = data["telefono"]
    cantidad_personas = data["cantidad_personas"]
    estado = data.get("estado", "reservada")

    if re.fullmatch(r'[A-Za-z0-9 ]+', nombre) is None or len(nombre) > 100:
        return 'nombre_invalido'
    if re.fullmatch(r'[A-Za-z0-9 ]+', apellido) is None or len(apellido) > 100:
        return 'nombre_invalido'
    if re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email) is None or len(email) > 100:
        return 'email_invalido'
    if re.fullmatch(r'\d{7,12}', str(dni)) is None:
        return 'dni_invalido'
    if estado not in ['reservada', 'cancelada', 'finalizada']:
        return 'estado_invalido'
    
    try:
        cantidad_personas = int(cantidad_personas)
        if cantidad_personas <= 0:
            return 'cantidad_invalida'
    except (ValueError, TypeError):
        return 'cantidad_invalida'

    try:
        resultado = insert_reserva(fecha, email, nombre, apellido, dni, servicio_id, telefono, cantidad_personas, estado)
        if resultado == 'duplicado':
            return 'reserva_duplicada'
        if resultado == 'servicio_no_existe':
            return 'servicio_no_encontrado'
        return 'exito', resultado
    except Exception:
        return 'error_db'

def actualizar_reserva(id, data):
    campos = ["fecha", "email", "nombre", "apellido", "DNI", "servicio_ID", "telefono", "cantidad_personas", "estado"]
    if not data or not all(k in data for k in campos):
        return 'body_invalido'

    fecha = data["fecha"]
    email = data["email"]
    nombre = data["nombre"]
    apellido = data["apellido"]
    dni = data["DNI"]
    servicio_id = data["servicio_ID"]
    telefono = data["telefono"]
    cantidad_personas = data["cantidad_personas"]
    estado = data["estado"]

    if re.fullmatch(r'[A-Za-z0-9 ]+', nombre) is None or len(nombre) > 100:
        return 'nombre_invalido'
    if re.fullmatch(r'[A-Za-z0-9 ]+', apellido) is None or len(apellido) > 100:
        return 'nombre_invalido'
    if re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email) is None or len(email) > 100:
        return 'email_invalido'
    if re.fullmatch(r'\d{7,12}', str(dni)) is None:
        return 'dni_invalido'
    if estado not in ['reservada', 'cancelada', 'finalizada']:
        return 'estado_invalido'

    try:
        cantidad_personas = int(cantidad_personas)
        if cantidad_personas <= 0:
            return 'cantidad_invalida'
    except (ValueError, TypeError):
        return 'cantidad_invalida'

    try:
        rows = update_reserva(id, fecha, email, nombre, apellido, dni, servicio_id, telefono, cantidad_personas, estado)
        if rows == 'servicio_no_existe':
            return 'servicio_no_encontrado'
    except Exception:
        return 'error_db'

    if not rows:
        return 'reserva_no_encontrada'
    
    return 'exito'

def obtener_reservas(base_url, query_params, limit, offset):
    reservas, total = seleccionar_reservas(limit, offset)
    if total == 0:
        raise ValueError("NOT_FOUND")

    args_for_links = query_params.copy()
    args_for_links.pop("_limit", None)
    args_for_links.pop("_offset", None)

    links = build_links(base_url, args_for_links, limit, offset, total)
    
    response_body = {
        "_links": links,
        "count": total,
        "data": reservas
    }
    return response_body

def obtener_reserva_por_id(id):
    try:
        reserva = seleccionar_unica_reserva(id)
        if not reserva:
            return 'reserva_no_encontrada'
        return 'exito', reserva
    except Exception:
        return 'error_db'