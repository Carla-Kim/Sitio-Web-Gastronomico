import logging
from flask import current_app

logger = logging.getLogger(__name__)

def enviar_confirmacion_reserva(usuario: dict, reserva: dict) -> None:
    asunto = 'Confirmación de tu reserva - Sitio Gastronómico'
    
    cuerpo = (
        f"¡Hola {usuario['nombre']}!\n\n"
        f"Tu reserva para el día {reserva['fecha']} ha sido confirmada con éxito.\n\n"
        f"Detalles de la reserva:\n"
        f"- Cantidad de personas: {reserva['cantidad_personas']}\n"
        f"- Teléfono de contacto: {reserva['telefono']}\n\n"
        f"¡Te esperamos!"
    )

    app_activa = current_app._get_current_object()
    mail = app_activa.extensions['mailman']

    mail.send_mail(
        subject=asunto,
        message=cuerpo,
        from_email=app_activa.config['MAIL_USERNAME'],
        recipient_list=[usuario['email']]
    )
    
    logger.info(f"Email enviado con éxito a {usuario['email']}")

def enviar_cancelacion_reserva(usuario: dict, reserva: dict) -> None:
    asunto = 'Cancelación de tu reserva - Sitio Gastronómico'
    
    cuerpo = (
        f"¡Hola {usuario['nombre']}!\n\n"
        f"Te informamos que tu reserva para el día {reserva['fecha']} ha sido cancelada con éxito.\n\n"
        f"Si no solicitaste este cambio o querés reprogramar, ponete en contacto con nosotros.\n\n"
        f"Saludos cordiales."
    )

    app_activa = current_app._get_current_object()
    mail = app_activa.extensions['mailman']

    mail.send_mail(
        subject=asunto,
        message=cuerpo,
        from_email=app_activa.config['MAIL_USERNAME'],
        recipient_list=[usuario['email']]
    )
    
    logger.info(f"Email de cancelación enviado con éxito a {usuario['email']}")