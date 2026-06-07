from .connection import get_connection

def obtener_resenas(limit, offset, sql_where, params_fechas):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        sql_count = f"SELECT COUNT(*) as count FROM Resenas {sql_where}"
        sql_elems = f"""
            SELECT resena_id, reserva_id, puntuacion_ambiente, puntuacion_servicio, puntuacion_comida 
            FROM Resenas 
            {sql_where}
            LIMIT %s OFFSET %s
        """
        cursor.execute(sql_count, tuple(params_fechas))
        res_count = cursor.fetchone()

        # count = res_count["count"] if isinstance(res_count, dict) else res_count[0]
        # error si devuelve un numero, no se puede acceder a count
        if isinstance(res_count, dict):
            count = res_count["count"]
        elif isinstance(res_count, (tuple, list)):
            count = res_count
        else:
            count = res_count

        params_elems = list(params_fechas) + [limit, offset]

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
        query = "SELECT * FROM Resenas WHERE resena_id = %s"
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
        query = "SELECT * FROM Resenas WHERE reserva_id = %s"
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
        query = f"SELECT AVG({columna_puntuacion}) as promedio FROM Resenas"
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
            INSERT INTO Resenas (reserva_id, puntuacion_ambiente, puntuacion_servicio, puntuacion_comida, comentario, fecha)
            VALUES (%s, %s, %s, %s, %s, CURDATE())
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

def borrar_resena(resena_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "DELETE FROM Resenas WHERE resena_id = %s"
        cursor.execute(query, (resena_id,))
        conn.commit()
        return cursor.rowcount
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        cursor.close()
        conn.close()