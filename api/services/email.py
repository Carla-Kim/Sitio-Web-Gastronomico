import logging
from flask_mailman import EmailMultiAlternatives
from flask import current_app, render_template

logger = logging.getLogger(__name__)

def enviar_confirmacion_reserva(usuario: dict, reserva: dict, qr_reserva=None, cancel_link=None) -> None:
    asunto = 'Confirmación de tu reserva - Sitio Gastronómico'
    
    html_cuerpo = render_template(
        "emails/confirmacion.html",
        usuario=usuario,
        reserva=reserva,
        cancel_link=cancel_link
    )

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

    logger.info(f"Email enviado con éxito a {usuario['email']}")

def enviar_cancelacion_reserva(usuario: dict, reserva: dict) -> None:
    asunto = 'Cancelación de tu reserva - Sitio Gastronómico'

    html_cuerpo = render_template(
        "emails/cancelada.html",
        usuario=usuario,
        reserva=reserva
    )

    app_activa = current_app._get_current_object()

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

    app_activa = current_app._get_current_object()

    msg = EmailMultiAlternatives(
        subject=asunto,
        body="Tu cliente de correo no soporta HTML.",
        from_email=app_activa.config['MAIL_USERNAME'],
        to=[usuario['email']]
    )

    msg.attach_alternative(html_cuerpo, "text/html")
    msg.send()
    
    logger.info(f"Email de agradecimiento enviado con éxito a {usuario['email']}")
