from supabase import create_client
from api.database.config import SUPABASE_BUCKET, SUPABASE_KEY, SUPABASE_URL
import uuid
import os
import base64

def _get_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase no esta configurado. Revisa el archivo .env")
        
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def extension_valida(filename):
    """Verifica que la extension del archivo sea permitida."""
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def subir_imagen(archivo) -> str | None:
    """
    Sube una imagen al bucket de Supabase Storage.
    Retorna el path del archivo en el bucket.
    """
    if not archivo or not archivo.filename:
        return None

    if not extension_valida(archivo.filename):
        raise ValueError("Formato de imagen no permitido")

    try:
        supabase = _get_client()
        extension = archivo.filename.rsplit('.', 1)[1].lower()

        # Generar nombre unico para evitar colisiones
        nombre_archivo = f"{uuid.uuid4().hex}.{extension}"
        contenido = archivo.read()

        content_type = archivo.content_type or 'image/jpeg'

        supabase.storage.from_(SUPABASE_BUCKET).upload(
            path=nombre_archivo,
            file=contenido,
            file_options={"content-type": content_type}
        )

        public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(nombre_archivo)
        return public_url

    except Exception as e:
        raise ValueError(f"Error al subir imagen a Supabase Storage: {e}")
