from database.connection import *


# Listar todos
def seleccionar_servicios_reserva():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT *
            FROM Servicios_reserva
            ORDER BY reserva_id
        """

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
        query = """
            SELECT *
            FROM Servicios_reserva
            WHERE reserva_id = %s
        """

        cursor.execute(query, [reserva_id])

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


# Asociar servicios
def insertar_servicios_reserva(reserva_id, servicios_ids):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        for servicio_id in servicios_ids:
            check_query = """
                SELECT servicio_reserva_id
                FROM Servicios_reserva
                WHERE reserva_id = %s
                AND servicios_id = %s
            """

            cursor.execute(
                check_query,
                [reserva_id, servicio_id]
            )

            exists = cursor.fetchone()

            if exists:
                return "CONFLICT"

            insert_query = """
                INSERT INTO Servicios_reserva (
                    reserva_id,
                    servicios_id
                )
                VALUES (%s, %s)
            """

            cursor.execute(
                insert_query,
                [reserva_id, servicio_id]
            )

        conn.commit()

    finally:
        cursor.close()
        conn.close()


# Eliminar servicios
def eliminar_servicios_reserva_db(reserva_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
            DELETE FROM Servicios_reserva
            WHERE reserva_id = %s
        """

        cursor.execute(query, [reserva_id])

        conn.commit()

        return cursor.rowcount

    finally:
        cursor.close()
        conn.close()