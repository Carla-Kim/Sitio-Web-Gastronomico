from .connection import get_connection
# Listar todos
def seleccionar_servicios_reserva():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """SELECT *FROM Servicios_reserva ORDER BY reserva_id"""
        cursor.execute(query)
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

# Listar por reserva
def seleccionar_servicios_por_reserva(reserva_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """SELECT *FROM Servicios_reserva WHERE reserva_id = %s"""
        cursor.execute(query, [reserva_id])

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

# Asociar servicios
import mysql.connector

import mysql.connector

def insertar_servicios_reserva(reserva_id, servicios_ids):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        for servicio_id in servicios_ids:
            check_query = """
                SELECT 1 FROM Servicios_reserva 
                WHERE reserva_id = %s AND servicio_id = %s
            """
            try:
                cursor.execute(check_query, [reserva_id, servicio_id])
                if cursor.fetchone():
                    return "CONFLICT"
            except mysql.connector.Error as e:
                if e.errno == 1054:
                    check_query_alt = """
                        SELECT 1 FROM Servicios_reserva 
                        WHERE reserva_id = %s AND servicio_ID = %s
                    """
                    cursor.execute(check_query_alt, [reserva_id, servicio_id])
                    if cursor.fetchone():
                        return "CONFLICT"
                else:
                    raise e

        insert_query = """
            INSERT INTO Servicios_reserva (reserva_id, servicio_id)
            VALUES (%s, %s)
        """
        for servicio_id in servicios_ids:
            try:
                cursor.execute(insert_query, [reserva_id, servicio_id])
            except mysql.connector.Error as e:
                if e.errno == 1054:
                    insert_query_alt = """
                        INSERT INTO Servicios_reserva (reserva_id, servicio_ID)
                        VALUES (%s, %s)
                    """
                    cursor.execute(insert_query_alt, [reserva_id, servicio_id])
                else:
                    raise e
            
        conn.commit()
        return "OK"

    except mysql.connector.Error as err:
        conn.rollback()
        if err.errno == 1452:
            return "NOT_FOUND"
        raise err
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        cursor.close()
        conn.close()


# Eliminar servicios
def eliminar_servicios_reserva_db(reserva_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """DELETE FROM Servicios_reserva WHERE reserva_id = %s"""
        cursor.execute(query, [reserva_id])
        conn.commit()

        return cursor.rowcount

    finally:
        cursor.close()
        conn.close()