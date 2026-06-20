import qrcode
import io
import os
from dotenv import load_dotenv

load_dotenv()


def _generar_qr_por_url(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    return img_buffer


def generar_qr_reserva(reserva_id):
    # URL que va a escanear el recepcionista en el local
    url_finalizar = f"http://localhost:5000/datos-reserva/{reserva_id}"
    return _generar_qr_por_url(url_finalizar)


def generar_qr_cancelacion(reserva_id):
    # URL que permite cancelar la reserva al escanear el código
    url_cancelar = f"http://localhost:5000/api/reservas/{reserva_id}/cancelar"
    return _generar_qr_por_url(url_cancelar)
