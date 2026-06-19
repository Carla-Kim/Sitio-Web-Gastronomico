from .connection import get_connection


# Obtiene la cantidad de mesas agrupadas por estado.
def obtener_conteo_mesas_db():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        query = """
            SELECT
                estado,
                cantidad_mesas
            FROM Mesas
        """

        cursor.execute(query)

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


# Actualiza la cantidad de mesas para un estado determinado.
def actualizar_cantidad_mesas_db(estado, cantidad_mesas):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        query = """
            UPDATE Mesas
            SET cantidad_mesas = %s
            WHERE estado = %s
        """

        cursor.execute(
            query,
            [cantidad_mesas, estado]
        )

        conn.commit()

        return cursor.rowcount

    finally:
        cursor.close()
        conn.close()

# Obtiene la cantidad de mesas para un estado específico.
def obtener_cantidad_por_estado_db(estado):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        query = """
            SELECT cantidad_mesas
            FROM Mesas
            WHERE estado = %s
        """

        cursor.execute(query, [estado])

        resultado = cursor.fetchone()

        if resultado:
            return resultado["cantidad_mesas"]

        return None

    finally:
        cursor.close()
        conn.close()
