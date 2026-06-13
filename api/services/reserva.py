import re
from api.database.reserva import *
from api.utils.pagination import build_links
from api.utils.qrcode_generator import generar_qr_reserva
import re
import logging
from api.services.email import enviar_confirmacion_reserva, enviar_cancelacion_reserva, enviar_mensaje_agradecimiento
from flask_mailman import EmailMessage
from flask import current_app

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
    estado = data.get("estado", "reservada")

    if re.fullmatch(r'[A-Za-z0-9 áéíóúÁÉÍÓÚñÑüÜ\'´`-]+', nombre) is None or len(nombre) > 100:
        return 'nombre_invalido'
    if re.fullmatch(r'[A-Za-z0-9 áéíóúÁÉÍÓÚñÑüÜ\'´`-]+', apellido) is None or len(apellido) > 100:
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
        resultado = insert_reserva(fecha, email, nombre, apellido, dni, telefono, cantidad_personas, estado)
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
                "nombre": f"{nombre} {apellido}",
                "email": email
            }
            reserva_datos = {
                "fecha": fecha,
                "cantidad_personas": cantidad_personas,
                "telefono": telefono
            }

            enviar_confirmacion_reserva(usuario=usuario_datos, reserva=reserva_datos)
            qr_generado = generar_qr_reserva(reserva_id=resultado)
            app_activa = current_app._get_current_object()
            
            msg_qr = EmailMessage(
                subject='Tu código de acceso - Sitio Gastronómico',
                body=f"¡Hola {nombre}! Adjuntamos el código QR correspondiente a tu reserva N° {resultado} para presentar en la entrada.",
                from_email=app_activa.config['MAIL_USERNAME'],
                to=[email]
            )
            msg_qr.attach(f"reserva_{resultado}.png", qr_generado.getvalue(), "image/png")
            msg_qr.send()
            
            logger.info(f"Mail independiente con QR enviado con éxito a {email}")
            
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

def escanear_y_finalizar_reserva(id):
    try:
        reserva = seleccionar_unica_reserva(id)
        if not reserva:
            return 'reserva_no_encontrada'
            
        if reserva['estado'] == 'finalizada':
            return 'reserva_ya_finalizada'
        if reserva['estado'] == 'cancelada':
            return 'reserva_cancelada'

        rows = cambiar_estado_finalizado(id)
        if not rows:
            return 'reserva_no_encontrada'
            
        return 'exito'
    except Exception as e:
        print(f"Error en servicio al finalizar reserva: {e}")
        return 'error_db'