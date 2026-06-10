from .connection import get_connection

def obtener_reservas_por_mes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
            SELECT
                MONTH(fecha) AS mes,
                COUNT(*) AS cantidad
            FROM Reservas
            GROUP BY MONTH(fecha)
            ORDER BY MONTH(fecha)
            """

    try:
        cursor.execute(query)
        reservas_por_mes = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    return reservas_por_mes

def obtener_usuarios_por_rol():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
            SELECT
                rol,
                COUNT(*) AS cantidad
            FROM Usuarios
            GROUP BY rol
            """

    try:
        cursor.execute(query)
        usuarios_por_rol = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    return usuarios_por_rol

def obtener_promedios_de_resenas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
            SELECT
                AVG(puntuacion_ambiente) AS ambiente,
                AVG(puntuacion_servicio) AS servicio,
                AVG(puntuacion_comida) AS comida
            FROM Resenas
            """

    try:
        cursor.execute(query)
        promedio_resenas = cursor.fetchone()

    finally:
        cursor.close()
        conn.close()

    return promedio_resenas

def obtener_productos_por_categoria():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
            SELECT
                c.nombre,
                COUNT(*) AS cantidad
            FROM Productos p
            JOIN Categorias c
                ON p.categorias_id = c.categorias_id
            GROUP BY c.categorias_id, c.nombre
            """

    try:
        cursor.execute(query)
        productos_por_categoria = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    return productos_por_categoria
