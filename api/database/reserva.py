import mysql.connector
from .config import DB_CONFIG, DB_NAME
from .connection import get_connection

import math

def insert_reserva(fecha, email, nombre, apellido, dni, telefono, cantidad_personas, comentario, estado):
    mesas_necesarias = math.ceil(cantidad_personas / 2)
    DURACION_RESERVA_HORAS = 2

    conn = get_connection()
    cursor = conn.cursor()
    try:
        check_query = """
            SELECT COUNT(*) 
            FROM Reservas 
            WHERE DNI = %s 
              AND fecha = %s 
              AND estado != 'cancelada'
        """
        cursor.execute(check_query, (dni, fecha))
        (existe,) = cursor.fetchone()
        
        if existe > 0:
            return 'duplicado_dni_horario'

        mesas_totales_query = "SELECT SUM(cantidad_mesas) FROM Mesas"
        cursor.execute(mesas_totales_query)
        (total_mesas,) = cursor.fetchone()
        
        if total_mesas is None:
            total_mesas = 0

        ocupacion_query = """
            SELECT cantidad_personas 
            FROM Reservas 
            WHERE estado NOT IN ('cancelada', 'finalizada')
              AND fecha < DATE_ADD(%s, INTERVAL %s HOUR)
              AND DATE_ADD(fecha, INTERVAL %s HOUR) > %s
        """
        cursor.execute(ocupacion_query, (fecha, DURACION_RESERVA_HORAS, DURACION_RESERVA_HORAS, fecha))
        reservas_en_rango = cursor.fetchall()
        
        mesas_ocupadas = 0
        for (cant,) in reservas_en_rango:
            mesas_ocupadas += math.ceil(cant / 2)
            
        if mesas_ocupadas + mesas_necesarias > total_mesas:
            return 'sin_capacidad_mesas'

        insert_query = """
            INSERT INTO Reservas (fecha, email, nombre, apellido, DNI, telefono, cantidad_personas, comentario, estado) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            insert_query, 
            (fecha, email, nombre, apellido, dni, telefono, cantidad_personas, comentario, estado)
        )
        conn.commit()
        return cursor.lastrowid

    except mysql.connector.Error as err:
        conn.rollback()
        if err.errno == 1062:
            return 'duplicado'
        raise err
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        cursor.close()
        conn.close()

def update_reserva(id, fecha, email, nombre, apellido, dni, telefono, cantidad_personas, estado):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Reservas SET fecha = %s, email = %s, nombre = %s, apellido = %s, DNI = %s, telefono = %s, cantidad_personas = %s, estado = %s WHERE reserva_id = %s",
            (fecha, email, nombre, apellido, dni, telefono, cantidad_personas, estado, id)
        )
        conn.commit()
        return cursor.rowcount
    except mysql.connector.Error as err:#Manejo de errores que uso despues en services y r
        conn.rollback()
        if err.errno == 1452:
            return 'servicio_no_existe'
        raise err
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        cursor.close()
        conn.close()

def seleccionar_reservas(limit, offset):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) AS total FROM Reservas")
        total = cursor.fetchone()['total']
        
        query = "SELECT * FROM Reservas ORDER BY reserva_id LIMIT %s OFFSET %s"
        cursor.execute(query, [limit, offset])
        reservas = cursor.fetchall()
        return reservas, total
    finally:
        cursor.close()
        conn.close()

def seleccionar_unica_reserva(id): #Borrar en caso de no ser necesaria utilizar
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM Reservas WHERE reserva_id = %s"
        cursor.execute(query, [id])
        reserva = cursor.fetchone()
        return reserva
    finally:
        cursor.close()
        conn.close()

def seleccionar_reservas_por_estado(estado, limit, offset): #Usamos paginacion también por si son muchas
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT COUNT(*) AS total FROM Reservas WHERE estado = %s"
        cursor.execute(query, [estado])
        total = cursor.fetchone()['total']
        
        query = "SELECT * FROM Reservas WHERE estado = %s ORDER BY reserva_id LIMIT %s OFFSET %s"
        cursor.execute(query, [estado, limit, offset])
        reservas = cursor.fetchall()
        return reservas, total
    finally:
        cursor.close()
        conn.close()

def cambiar_estado_cancelado(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)    
    try:
        query_datos = "SELECT nombre, email, fecha, cantidad_personas, estado FROM Reservas WHERE reserva_id = %s"
        cursor.execute(query_datos, (id,))
        datos_reserva = cursor.fetchone()

        if not datos_reserva:
            return 0, None
        if datos_reserva['estado'] == 'finalizada':
            return 'reserva_ya_finalizada', None
        if datos_reserva['estado'] == 'cancelada':
            return 0, None

        mesas_a_liberar = math.ceil(datos_reserva['cantidad_personas'] / 2)

        query_update = "UPDATE Reservas SET estado = 'cancelada' WHERE reserva_id = %s"
        cursor.execute(query_update, (id,))

        cursor.execute(
            "UPDATE Mesas SET cantidad_mesas = cantidad_mesas - %s WHERE estado = 'ocupada'",
            (mesas_a_liberar,)
        )
        cursor.execute(
            "UPDATE Mesas SET cantidad_mesas = cantidad_mesas + %s WHERE estado = 'desocupada'",
            (mesas_a_liberar,)
        )
        conn.commit()
        return cursor.rowcount, datos_reserva
    except Exception as e:
        conn.rollback()
        print(f"Error en DB al cancelar: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()

def seleccionar_reservas_por_fecha(fecha, limit, offset):#Misma lógica que la anterior, tal vez optimizable.
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT COUNT(*) AS total FROM Reservas WHERE DATE(fecha) = %s"
        cursor.execute(query, [fecha])
        total = cursor.fetchone()['total']
        
        query = "SELECT * FROM Reservas WHERE DATE(fecha) = %s ORDER BY reserva_id LIMIT %s OFFSET %s"
        cursor.execute(query, [fecha, limit, offset])
        reservas = cursor.fetchall()
        return reservas, total
    finally:
        cursor.close()
        conn.close()

def cambiar_estado_finalizado(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)    
    try:
        query_datos = "SELECT cantidad_personas, estado FROM Reservas WHERE reserva_id = %s"
        cursor.execute(query_datos, (id,))
        datos_reserva = cursor.fetchone()

        if not datos_reserva or datos_reserva['estado'] == 'finalizada':
            return 0

        mesas_a_liberar = math.ceil(datos_reserva['cantidad_personas'] / 2)

        query = "UPDATE Reservas SET estado = 'finalizada' WHERE reserva_id = %s"
        cursor.execute(query, (id,))

        cursor.execute(
            "UPDATE Mesas SET cantidad_mesas = cantidad_mesas - %s WHERE estado = 'ocupada'",
            (mesas_a_liberar,)
        )
        cursor.execute(
            "UPDATE Mesas SET cantidad_mesas = cantidad_mesas + %s WHERE estado = 'desocupada'",
            (mesas_a_liberar,)
        )

        conn.commit()
        return cursor.rowcount
    except Exception as e:
        conn.rollback()
        print(f"Error en DB al finalizar por QR: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()