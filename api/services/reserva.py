import re
import logging
from flask import current_app
from api.database.reserva import *
from api.utils.pagination import build_links
from api.utils.qrcode_generator import generar_qr_reserva
from api.services.email import enviar_confirmacion_reserva, enviar_cancelacion_reserva, enviar_mensaje_agradecimiento

logger = logging.getLogger(__name__)

def crear_reserva(data):
    campos = ["fecha", "email", "nombre", "apellido", "DNI", "telefono", "cantidad_personas"]
    if not data or not all(i in data for i in campos):
        return 'body_invalido'
    
    fecha = data["fecha"]
    email = data["email"]
    nombre = data["nombre"]
    apellido = data["apellido"]
    dni = data["DNI"]
    telefono = data["telefono"]
    cantidad_personas = data["cantidad_personas"]
    comentario = data.get("comentario", None)
    estado = data.get("estado", "reservada")

    if re.fullmatch(r'[A-Za-z0-9\sáéíóúÁÉÍÓÚñÑüÜ''-]+', nombre) is None or len(nombre) > 100:
        return 'nombre_invalido'
    if re.fullmatch(r'[A-Za-z0-9\sáéíóúÁÉÍÓÚñÑüÜ\'´-]+', apellido) is None or len(apellido) > 100:
        return 'apellido_invalido'
    if re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email) is None or len(email) > 100:
        return 'email_invalido'
    if re.fullmatch(r'\d{7,12}', str(dni)) is None:
        return 'dni_invalido'
    
    try:
        cantidad_personas = int(cantidad_personas)
        if cantidad_personas <= 0:
            return 'cantidad_invalida'
    except (ValueError, TypeError):
        return 'cantidad_invalida'

    try:
        resultado = insert_reserva(fecha, email, nombre, apellido, dni, telefono, cantidad_personas, comentario, estado)
        if resultado == 'duplicado':
            return 'reserva_duplicada'
        if resultado == 'servicio_no_existe':
            return 'servicio_no_encontrado'
        if resultado == 'duplicado_dni_horario':
            return 'reserva_duplicada_horario'
        if resultado == 'sin_capacidad_mesas':
            return 'sin_disponibilidad'
        
        try:
            usuario_datos = {
                "nombre": nombre,
                "apellido": apellido,
                "email": email,
                "dni": dni
            }
            reserva_datos = {
                "id": resultado,
                "fecha": fecha,
                "cantidad_personas": cantidad_personas,
                "telefono": telefono
            }

            qr_reserva = generar_qr_reserva(reserva_id=resultado)
            frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:5000')
            cancel_link = f"{frontend_url}/cancelar?id={resultado}"
            enviar_confirmacion_reserva(
                usuario=usuario_datos,
                reserva=reserva_datos,
                qr_reserva=qr_reserva,
                cancel_link=cancel_link
            )
            
        except Exception as email_error:
            logger.error(f"La reserva se creó pero falló el envío del mail: {email_error}")

        return 'exito', resultado
        
    except Exception as e:
        print(f"Error real en la base de datos: {e}")
        return 'error_db'

def actualizar_reserva(id, data):
    campos = ["fecha", "email", "nombre", "apellido", "DNI", "telefono", "cantidad_personas", "estado"]
    if not data or not all(k in data for k in campos):
        return 'body_invalido'

    fecha = data["fecha"]
    email = data["email"]
    nombre = data["nombre"]
    apellido = data["apellido"]
    dni = data["DNI"]
    telefono = data["telefono"]
    cantidad_personas = data["cantidad_personas"]
    estado = data["estado"]

    if re.fullmatch(r'[A-Za-z0-9 áéíóúÁÉÍÓÚñÑüÜ\'´`-]+', nombre) is None or len(nombre) > 100:
        return 'nombre_invalido'
    if re.fullmatch(r'[A-Za-z0-9 áéíóúÁÉÍÓÚñÑüÜ\'´`-]+', apellido) is None or len(apellido) > 100:
        return 'apellido_invalido'
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
        rows = update_reserva(id, fecha, email, nombre, apellido, dni, telefono, cantidad_personas, estado)
        if rows == 'servicio_no_existe':
            return 'servicio_no_encontrado'
        if not rows:
            return 'reserva_no_encontrada'
        return 'exito'
    except Exception:
        return 'error_db'

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

def filtrar_por_estado(base_url, query_params, estado, limit, offset):
    if estado not in ['reservada', 'cancelada', 'finalizada']:
        return 'estado_invalido'
    
    try:
        reservas, total = seleccionar_reservas_por_estado(estado, limit, offset)
        if total == 0:
            return 'no_encontrado'
    except Exception:
        return 'error_db'

    args_for_links = query_params.copy()
    args_for_links.pop("_limit", None)
    args_for_links.pop("_offset", None)

    links = build_links(base_url, args_for_links, limit, offset, total)
    
    response_body = {
        "_links": links,
        "count": total,
        "data": reservas
    }
    return 'exito', response_body
    
def cancelar_reserva(id):
    if id is None or id <= 0:
        return 'id_invalido'
    try:
        reserva = seleccionar_unica_reserva(id)
        if not reserva:
            return 'reserva_no_encontrada'
        if reserva['estado'] == 'finalizada':
            return 'reserva_ya_finalizada'
        if reserva['estado'] == 'cancelada':
            return 'reserva_ya_cancelada'

        rows, datos = cambiar_estado_cancelado(id)
        if rows == 'reserva_ya_finalizada':
            return 'reserva_ya_finalizada'
        if not rows:
            return 'reserva_no_encontrada'

        try:
            usuario_datos = {
                "nombre": reserva["nombre"],
                "email": reserva["email"]
            }
            reserva_datos = {
                "fecha": reserva["fecha"]
            }
            enviar_cancelacion_reserva(usuario=usuario_datos, reserva=reserva_datos)
        except Exception as email_error:
            logger.error(f"La reserva se canceló pero falló el envío del mail: {email_error}")

        return 'exito', {"message": f"Reserva {id} cancelada correctamente"}
    except Exception:
        return 'error_db'

def obtener_reservas_por_fecha(base_url, query_params, fecha, limit, offset):
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(fecha)) is None:
        return 'fecha_invalida'

    try:
        reservas, total = seleccionar_reservas_por_fecha(fecha, limit, offset)
        if total == 0:
            return 'no_encontrado'
    except Exception:
        return 'error_db'

    args_for_links = query_params.copy()
    args_for_links.pop("_limit", None)
    args_for_links.pop("_offset", None)

    links = build_links(base_url, args_for_links, limit, offset, total)
    
    response_body = {
        "_links": links,
        "count": total,
        "data": reservas
    }
    return 'exito', response_body

def escanear_y_finalizar_reserva(id):
    if id is None or id <= 0:
        return 'id_invalido'
    try:
        reserva = seleccionar_unica_reserva(id)
        if not reserva:
            return 'reserva_no_encontrada'
            
        estado_actual = reserva.get('estado')
        if estado_actual == 'finalizada':
            return 'reserva_ya_finalizada'
        if estado_actual == 'cancelada':
            return 'reserva_cancelada'
            
        rows = cambiar_estado_finalizado(id)
        if rows == 'reserva_ya_finalizada':
            return 'reserva_ya_finalizada'
        if not rows:
            return 'reserva_no_encontrada'
            
        try:
            usuario_datos = {
                "nombre": reserva["nombre"],
                "email": reserva["email"]
            }
            frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:5000')
            form_link = (
                f"{frontend_url}/calificar"
                f"?reserva_id={id}"
            )
            enviar_mensaje_agradecimiento(usuario=usuario_datos, reserva=reserva, form_link=form_link)
        except Exception as email_error:
            logger.error(f"La reserva se finalizó pero falló el envío del mail: {email_error}")
            
        return 'exito'
    except Exception:
        return 'error_db'