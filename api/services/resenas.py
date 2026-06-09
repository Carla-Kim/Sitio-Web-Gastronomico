from api.database import resenas as resenas_db
from api.utils.pagination import build_links


def listar_resenas(base_url, limit, offset, fecha_desde=None, fecha_hasta=None, p_ambiente=None, p_servicio=None, p_comida=None):
    where_clauses = []
    params_filtros = []

    if fecha_desde:
        where_clauses.append("res.fecha >= %s")
        params_filtros.append(fecha_desde)
        
    if fecha_hasta:
        where_clauses.append("res.fecha <= %s")
        params_filtros.append(fecha_hasta)

    if p_ambiente is not None:
        if not (1 <= p_ambiente <= 5):
            raise ValueError("BAD_REQUEST")
        where_clauses.append("res.puntuacion_ambiente = %s")
        params_filtros.append(p_ambiente)

    if p_servicio is not None:
        if not (1 <= p_servicio <= 5):
            raise ValueError("BAD_REQUEST")
        where_clauses.append("res.puntuacion_servicio = %s")
        params_filtros.append(p_servicio)

    if p_comida is not None:
        if not (1 <= p_comida <= 5):
            raise ValueError("BAD_REQUEST")
        where_clauses.append("res.puntuacion_comida = %s")
        params_filtros.append(p_comida)

    sql_where = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    try:
         resenas_data = resenas_db.obtener_resenas(limit, offset, sql_where, params_filtros)
    except Exception:
        raise ValueError("BAD_REQUEST")

    if not resenas_data or resenas_data.get("data") is None:
        raise ValueError("NOT_FOUND")

    try:
        resenas_formateadas = [{
                "resena_id": r["resena_id"],
                "reserva_id": r["reserva_id"],
                "nombre_usuario": r["nombre_usuario"],
                "comentario": r["comentario"],
                "puntuacion_ambiente": r["puntuacion_ambiente"],
                "puntuacion_servicio": r["puntuacion_servicio"],
                "puntuacion_comida": r["puntuacion_comida"],
                "fecha": r["fecha"].isoformat() if r["fecha"] else None
            } for r in resenas_data["data"]] 
        
        count = resenas_data["count"]
        
        filtros_actuales = {}
        if fecha_desde: 
            filtros_actuales["fecha_desde"] = fecha_desde
        if fecha_hasta: 
            filtros_actuales["fecha_hasta"] = fecha_hasta 
        if p_ambiente is not None:
            filtros_actuales["puntaje_ambiente"] = p_ambiente
        if p_servicio is not None:
            filtros_actuales["puntaje_servicio"] = p_servicio
        if p_comida is not None:
            filtros_actuales["puntaje_comida"] = p_comida

        return {
            "resenas": resenas_formateadas,
            "count": count,
            "_links": build_links(base_url, filtros_actuales, limit, offset, count)
        }
    except KeyError:
        raise ValueError("BAD_REQUEST")

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

    estado_reserva = resenas_db.check_reserva_existe_y_finalizada(reserva_id)
    if estado_reserva == "NO_EXISTE":
        raise ValueError("NO_EXISTE")
    if estado_reserva == "NO_FINALIZADA":
        raise ValueError("BAD_REQUEST") 

    if resenas_db.check_resena_existe_por_reserva(reserva_id):
        raise ValueError("CONFLICT")

    nuevo_id = resenas_db.ingresar_resena(reserva_id, p_ambiente, p_servicio, p_comida, comentario)
    
    return {
        "status": "success",
        "message": "Reseña creada correctamente.",
        "resena_id": nuevo_id
    }

def buscar_por_id(resena_id):
    if resena_id is None or resena_id <= 0:
        raise ValueError("BAD_REQUEST")
    
    resena = resenas_db.obtener_por_id(resena_id)
    if not resena:
        raise ValueError("NOT_FOUND")
    return resena

def buscar_por_reserva(reserva_id):
    if reserva_id is None or reserva_id <= 0:
        raise ValueError("BAD_REQUEST")
        
    resena = resenas_db.obtener_por_reserva(reserva_id)
    if not resena:
        raise ValueError("NOT_FOUND")
    return resena

def obtener_promedio(columna):
    try:
        promedio = resenas_db.obtener_promedio_columna(columna)
    except ValueError:
        raise ValueError("BAD_REQUEST")
        
    if promedio is None:
        raise ValueError("NOT_FOUND")
    return {"promedio": round(float(promedio), 2)}


def eliminar_resena(resena_id):
    if resena_id is None or resena_id <= 0:
        raise ValueError("BAD_REQUEST")
        
    filas_borradas = resenas_db.borrar_resena(resena_id)
    if filas_borradas == 0:
        raise ValueError("NOT_FOUND")
