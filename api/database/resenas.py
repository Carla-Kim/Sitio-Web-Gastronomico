from .connection import get_connection

def obtener_resenas(limit, offset, sql_where, params_filtros):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        sql_count = f"SELECT COUNT(*) as count FROM Resenas res JOIN Reservas r ON res.reserva_id = r.reserva_id {sql_where}"
        cursor.execute(sql_count, tuple(params_filtros))
        res_count = cursor.fetchone()
        
        count = res_count["count"] if res_count else 0

        sql_elems = f"""
            SELECT res.resena_id, res.reserva_id, res.puntuacion_ambiente, res.puntuacion_servicio, res.puntuacion_comida, res.comentario, res.fecha, res.estado,
            CONCAT(r.nombre, ' ', r.apellido) as nombre_usuario
            FROM Resenas res
            JOIN Reservas r ON res.reserva_id = r.reserva_id
            {sql_where}
            LIMIT %s OFFSET %s"""
        
        params_elems = list(params_filtros) + [limit, offset]

        cursor.execute(sql_elems, tuple(params_elems))
        rows = cursor.fetchall()

        return {
            "data": rows, 
            "count": count
        }
    except Exception as err:
        raise err
    finally:
        cursor.close()
        conn.close()

def obtener_por_id(resena_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """SELECT res.*, CONCAT(r.nombre, ' ', r.apellido) as nombre_usuario
            FROM Resenas res
            JOIN Reservas r ON res.reserva_id = r.reserva_id
            WHERE res.resena_id = %s"""
        cursor.execute(query, (resena_id,))
        return cursor.fetchone()
    except Exception as err:
        raise err
    finally:
        cursor.close()
        conn.close()

def obtener_por_reserva(reserva_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """SELECT res.*, CONCAT(r.nombre, ' ', r.apellido) as nombre_usuario
            FROM Resenas res
            JOIN Reservas r ON res.reserva_id = r.reserva_id
            WHERE res.reserva_id = %s"""
        cursor.execute(query, (reserva_id,))
        return cursor.fetchone()
    except Exception as err:
        raise err
    finally:
        cursor.close()
        conn.close()

def obtener_promedio_columna(columna_puntuacion):
    if columna_puntuacion not in ['puntuacion_ambiente', 'puntuacion_servicio', 'puntuacion_comida']:
        raise ValueError("Columna inválida")
        
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = f"SELECT AVG({columna_puntuacion}) as promedio FROM Resenas WHERE estado = 'habilitada'"
        cursor.execute(query)
        result = cursor.fetchone()
        return result["promedio"] if result else None
    except Exception as err:
        raise err
    finally:
        cursor.close()
        conn.close()

def check_reserva_existe_y_finalizada(reserva_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT estado FROM Reservas WHERE reserva_id = %s"
        cursor.execute(query, (reserva_id,))
        reserva = cursor.fetchone()
        if not reserva:
            return "NO_EXISTE"
        if reserva["estado"] != "finalizada":
            return "NO_FINALIZADA"
        return "OK"
    except Exception as err:
        raise err
    finally:
        cursor.close()
        conn.close()

def check_resena_existe_por_reserva(reserva_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT 1 FROM Resenas WHERE reserva_id = %s"
        cursor.execute(query, (reserva_id,))
        return cursor.fetchone() is not None
    except Exception as err:
        raise err
    finally:
        cursor.close()
        conn.close()

def ingresar_resena(reserva_id, puntuacion_ambiente, puntuacion_servicio, puntuacion_comida, comentario):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO Resenas (reserva_id, puntuacion_ambiente, puntuacion_servicio, puntuacion_comida, comentario, fecha, estado)
            VALUES (%s, %s, %s, %s, %s, CURDATE(), 'habilitada')
        """
        cursor.execute(query, (reserva_id, puntuacion_ambiente, puntuacion_servicio, puntuacion_comida, comentario))
        conn.commit()
        return cursor.lastrowid
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        cursor.close()
        conn.close()

def cambiar_estado_resena(resena_id, nuevo_estado):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "UPDATE Resenas SET estado = %s WHERE resena_id = %s"
        cursor.execute(query, (nuevo_estado, resena_id))
        conn.commit()
        return cursor.rowcount
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        cursor.close()
        conn.close()