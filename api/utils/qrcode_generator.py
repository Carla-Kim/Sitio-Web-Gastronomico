import qrcode
import io
import os
from dotenv import load_dotenv

load_dotenv()

def generar_qr_reserva(reserva_id):
    # URL que va a escanear el recepcionista en el local
    base_url = os.getenv("APP_BASE_URL", "http://localhost:5000")

    url_finalizar = f"{base_url}/reservas/{reserva_id}/escanear"
    print(f"--- URL DENTRO DEL QR: {url_finalizar} ---")

    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url_finalizar)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    
    return img_buffer