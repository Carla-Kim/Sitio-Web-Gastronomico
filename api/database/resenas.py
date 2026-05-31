def obtener_resenas(cursor, limit, offset):
    sql_count = "SELECT COUNT(*) as count FROM Resenas"
    sql_elems = """
        SELECT resena_id, reserva_id, puntuacion_ambiente, puntuacion_servicio, puntuacion_comida 
        FROM Resenas 
        LIMIT %s OFFSET %s
    """
    cursor.execute(sql_count)
    count = cursor.fetchone()["count"]

    cursor.execute(sql_elems, (limit, offset))
    rows = cursor.fetchall()

    return {
        "data": rows, 
        "count": count
    }

def obtener_por_id(cursor, resena_id):
    query = "SELECT * FROM Resenas WHERE resena_id = %s"
    cursor.execute(query, (resena_id,))
    return cursor.fetchone()

def obtener_por_reserva(cursor, reserva_id):
    query = "SELECT * FROM Resenas WHERE reserva_id = %s"
    cursor.execute(query, (reserva_id,))
    return cursor.fetchone()

def obtener_promedio_columna(cursor, columna_puntuacion):
    if columna_puntuacion not in ['puntuacion_ambiente', 'puntuacion_servicio', 'puntuacion_comida']:
        raise ValueError("Columna inválida")
        
    query = f"SELECT AVG({columna_puntuacion}) as promedio FROM Resenas"
    cursor.execute(query)
    result = cursor.fetchone()
    return result["promedio"] if result else None

def check_reserva_existe_y_finalizada(cursor, reserva_id):
    query = "SELECT estado FROM Reservas WHERE reserva_id = %s"
    cursor.execute(query, (reserva_id,))
    reserva = cursor.fetchone()
    if not reserva:
        return "NO_EXISTE"
    if reserva["estado"] != "finalizada":
        return "NO_FINALIZADA"
    return "OK"

def check_resena_existe_por_reserva(cursor, reserva_id):
    query = "SELECT 1 FROM Resenas WHERE reserva_id = %s"
    cursor.execute(query, (reserva_id,))
    return cursor.fetchone() is not None

def ingresar_resena(cursor, reserva_id, puntuacion_ambiente, puntuacion_servicio, puntuacion_comida, comentario):
    query = """
        INSERT INTO Resenas (reserva_id, puntuacion_ambiente, puntuacion_servicio, puntuacion_comida, comentario, fecha)
        VALUES (%s, %s, %s, %s, %s, CURDATE())
    """
    cursor.execute(query, (reserva_id, puntuacion_ambiente, puntuacion_servicio, puntuacion_comida, comentario))
    return cursor.lastrowid

def borrar_resena(cursor, resena_id):
    query = "DELETE FROM Resenas WHERE resena_id = %s"
    cursor.execute(query, (resena_id,))
    return cursor.rowcount