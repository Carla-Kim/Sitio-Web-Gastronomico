import logging
from flask_mailman import EmailMultiAlternatives
from flask import current_app, render_template

logger = logging.getLogger(__name__)

def enviar_confirmacion_reserva(usuario: dict, reserva: dict, qr_reserva=None, cancel_link=None) -> None:
    asunto = 'Confirmación de tu reserva - Sitio Gastronómico'
    # nombre_completo = f"{usuario.get('nombre', '')} {usuario.get('apellido', '')}".strip()
    
    html_cuerpo = render_template(
        "emails/confirmacion.html",
        usuario=usuario,
        reserva=reserva,
        cancel_link=cancel_link
    )

    # cuerpo = (
    #     f"¡Hola {nombre_completo}!\n\n"
    #     f"Tu reserva para el día {reserva['fecha']} ha sido confirmada con éxito.\n\n"
    #     f"Detalles de la reserva:\n"
    #     f"- Número de reserva: {reserva.get('id', 'N/A')}\n"
    #     f"- Fecha y hora: {reserva['fecha']}\n"
    #     f"- Cantidad de personas: {reserva['cantidad_personas']}\n"
    #     f"- Teléfono de contacto: {reserva['telefono']}\n"
    #     f"- DNI: {usuario.get('dni', 'N/A')}\n"
    #     f"- Email de contacto: {usuario.get('email', 'N/A')}\n\n"
    #     f"Adjuntamos el código QR de reserva en este correo. Presentalo en la entrada para acceder al local.\n"
    # )


    app_activa = current_app._get_current_object()

    msg = EmailMultiAlternatives(
        subject=asunto,
        body="Tu cliente de correo no soporta HTML.",
        from_email=app_activa.config['MAIL_USERNAME'],
        to=[usuario['email']]
    )

    msg.attach_alternative(html_cuerpo, "text/html")
       
    if qr_reserva:
        msg.attach(f"reserva_{reserva.get('id', 'reserva')}.png", qr_reserva.getvalue(), "image/png")
    msg.send()
    # else:
    #     mail = app_activa.extensions['mailman']
    #     mail.send_mail(
    #         subject=asunto,
    #         message=cuerpo,
    #         from_email=app_activa.config['MAIL_USERNAME'],
    #         recipient_list=[usuario['email']]
    #     )

    logger.info(f"Email enviado con éxito a {usuario['email']}")

def enviar_cancelacion_reserva(usuario: dict, reserva: dict) -> None:
    asunto = 'Cancelación de tu reserva - Sitio Gastronómico'
    
    # cuerpo = (
    #     f"¡Hola {usuario['nombre']}!\n\n"
    #     f"Te informamos que tu reserva para el día {reserva['fecha']} ha sido cancelada con éxito.\n\n"
    #     f"Si no solicitaste este cambio o querés reprogramar, ponete en contacto con nosotros.\n\n"
    #     f"Saludos cordiales."
    # )

    html_cuerpo = render_template(
        "emails/cancelada.html",
        usuario=usuario,
        reserva=reserva
    )

    app_activa = current_app._get_current_object()
    # mail = app_activa.extensions['mailman']

    msg = EmailMultiAlternatives(
        subject=asunto,
        body="Tu cliente de correo no soporta HTML.",
        from_email=app_activa.config['MAIL_USERNAME'],
        to=[usuario['email']]
    )

    msg.attach_alternative(html_cuerpo, "text/html")
    msg.send()
    
    logger.info(f"Email de cancelación enviado con éxito a {usuario['email']}")

def enviar_mensaje_agradecimiento(usuario: dict, reserva: dict, form_link=None) -> None:
    asunto = 'Muchas gracias por venir a nuestro local - Sitio Gastronómico'
    
    html_cuerpo = render_template(
        "emails/calificar.html",
        usuario=usuario,
        reserva=reserva,
        form_link=form_link
    )

    # cuerpo = (
    #     f"¡Hola {usuario['nombre']}!\n\n"
    #     f"Muchisimas gracias por disfrutar de nuestra comida en Sitio Gastronómico.\n\n"
    #     f"Tu opinión es importante para mejorar nuestro local. Por favor, completa el siguiente form dejando tu reseña.\n\n"
    #     f"Saludos cordiales."
    # )

    app_activa = current_app._get_current_object()
    # mail = app_activa.extensions['mailman']

    msg = EmailMultiAlternatives(
        subject=asunto,
        body="Tu cliente de correo no soporta HTML.",
        from_email=app_activa.config['MAIL_USERNAME'],
        to=[usuario['email']]
    )

    msg.attach_alternative(html_cuerpo, "text/html")
    msg.send()
    
    logger.info(f"Email de agradecimiento enviado con éxito a {usuario['email']}")