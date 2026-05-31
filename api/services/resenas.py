from api.database import resenas as resenas_db
from api.database.connection import get_cursor
from api.utils.pagination import build_links

def listar_resenas(base_url, limit, offset):
    with get_cursor() as cursor:
        resenas_data = resenas_db.obtener_resenas(cursor, limit, offset)

        if not resenas_data or not resenas_data.get("data"):
            raise ValueError("NOT_FOUND")

        resenas_formateadas = [{
            "resena_id": r["resena_id"],
            "reserva_id": r["reserva_id"],
            "puntuacion_ambiente": r["puntuacion_ambiente"],
            "puntuacion_servicio": r["puntuacion_servicio"],
            "puntuacion_comida": r["puntuacion_comida"]
        } for r in resenas_data["data"]] 

        count = resenas_data["count"]
        
    return {
        "resenas": resenas_formateadas,
        "_links": build_links(base_url, {}, limit, offset, count)
    }


def buscar_por_id(resena_id):
    if resena_id is None or resena_id <= 0:
        raise ValueError("BAD_REQUEST")
        
    with get_cursor() as cursor:
        resena = resenas_db.obtener_por_id(cursor, resena_id)
        if not resena:
            raise ValueError("NOT_FOUND")
        return resena


def buscar_por_reserva(reserva_id):
    if reserva_id is None or reserva_id <= 0:
        raise ValueError("BAD_REQUEST")
        
    with get_cursor() as cursor:
        resena = resenas_db.obtener_por_reserva(cursor, reserva_id)
        if not resena:
            raise ValueError("NOT_FOUND")
        return resena


def obtener_promedio(columna):
    with get_cursor() as cursor:
        promedio = resenas_db.obtener_promedio_columna(cursor, columna)
        if promedio is None:
            raise ValueError("NOT_FOUND")
        return {"promedio": round(float(promedio), 2)}


def crear_resena(data):
    if not data:
        raise ValueError("BAD_REQUEST")

    reserva_id = data.get('reserva_id')
    p_ambiente = data.get('puntaje_ambiente')
    p_servicio = data.get('puntaje_servicio')
    p_comida = data.get('puntaje_comida')
    comentario = data.get('comentario', None)

    if not all([reserva_id, p_ambiente, p_servicio, p_comida]):
        raise ValueError("BAD_REQUEST")

    for p in [p_ambiente, p_servicio, p_comida]:
        if not isinstance(p, int) or p < 1 or p > 5:
            raise ValueError("BAD_REQUEST")

    with get_cursor() as cursor:
        estado_reserva = resenas_db.check_reserva_existe_y_finalizada(cursor, reserva_id)
        if estado_reserva == "NO_EXISTE":
            raise ValueError("NO_EXISTE")
        if estado_reserva == "NO_FINALIZADA":
            raise ValueError("BAD_REQUEST") 

        if resenas_db.check_resena_existe_por_reserva(cursor, reserva_id):
            raise ValueError("CONFLICT")

        nuevo_id = resenas_db.ingresar_resena(cursor, reserva_id, p_ambiente, p_servicio, p_comida, comentario)
        
        return {
            "status": "success",
            "message": "Reseña creada correctamente.",
            "resena_id": nuevo_id
        }


def eliminar_resena(resena_id):
    if resena_id is None or resena_id <= 0:
        raise ValueError("BAD_REQUEST")
        
    with get_cursor() as cursor:
        filas_borradas = resenas_db.borrar_resena(cursor, resena_id)
        if filas_borradas == 0:
            raise ValueError("NOT_FOUND")