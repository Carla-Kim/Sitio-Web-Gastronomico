import logging
from flask_mailman import EmailMessage
from flask import current_app

logger = logging.getLogger(__name__)

def enviar_confirmacion_reserva(usuario: dict, reserva: dict, qr_reserva=None, qr_cancelacion=None) -> None:
    asunto = 'Confirmación de tu reserva - Sitio Gastronómico'
    
    cuerpo = (
        f"¡Hola {usuario['nombre']}!\n\n"
        f"Tu reserva para el día {reserva['fecha']} ha sido confirmada con éxito.\n\n"
        f"Detalles de la reserva:\n"
        f"- Cantidad de personas: {reserva['cantidad_personas']}\n"
        f"- Teléfono de contacto: {reserva['telefono']}\n\n"
        f"Adjuntamos dos códigos QR en este correo:\n"
        f"1) Código QR de reserva: presentalo en la entrada para acceder al local.\n"
        f"2) Código QR de cancelación: usalo si necesitas cancelar tu reserva.\n\n"
        f"¡Te esperamos!"
    )

    app_activa = current_app._get_current_object()

    if qr_reserva or qr_cancelacion:
        msg = EmailMessage(
            subject=asunto,
            body=cuerpo,
            from_email=app_activa.config['MAIL_USERNAME'],
            to=[usuario['email']]
        )
        if qr_reserva is not None:
            msg.attach(f"reserva_{reserva.get('id', 'reserva')}.png", qr_reserva.getvalue(), "image/png")
        if qr_cancelacion is not None:
            msg.attach(f"cancelacion_{reserva.get('id', 'reserva')}.png", qr_cancelacion.getvalue(), "image/png")
        msg.send()
    else:
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

def enviar_mensaje_agradecimiento(usuario: dict, reserva: dict) -> None:
    asunto = 'Muchas gracias por venir a nuestro local - Sitio Gastronómico'
    
    cuerpo = (
        f"¡Hola {usuario['nombre']}!\n\n"
        f"Muchisimas gracias por disfrutar de nuestra comida en Sitio Gastronómico.\n\n"
        f"Tu opinión es importante para mejorar nuestro local. Por favor, completa el siguiente form dejando tu reseña.\n\n"
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
    
    logger.info(f"Email de reserva enviado con éxito a {usuario['email']}")