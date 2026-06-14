from .connection import get_connection

# Obtiene la cantidad de reservas agrupadas por estado.
def obtener_reservas_por_estado():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            estado,
            COUNT(*) AS cantidad
        FROM Reservas
        GROUP BY estado
        ORDER BY estado
    """

    try:
        cursor.execute(query)
        reservas_por_estado = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    return reservas_por_estado


# Obtiene la cantidad de reservas agrupadas por mes.
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


# Obtiene la cantidad de productos y el precio promedio por categoría.
def obtener_productos_por_categoria():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            c.nombre,
            COUNT(*) AS cantidad,
            AVG(p.precio) AS precio_promedio
        FROM Productos p
        JOIN Categorias c
            ON p.categorias_id = c.categorias_id
        GROUP BY c.categorias_id, c.nombre
        ORDER BY c.nombre
    """

    try:
        cursor.execute(query)
        productos_por_categoria = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    return productos_por_categoria


# Obtiene el promedio de puntuaciones de las reseñas habilitadas.
def obtener_promedio_resenas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            AVG(puntuacion_ambiente) AS ambiente,
            AVG(puntuacion_servicio) AS servicio,
            AVG(puntuacion_comida) AS comida,
            (
                AVG(puntuacion_ambiente) +
                AVG(puntuacion_servicio) +
                AVG(puntuacion_comida)
            ) / 3 AS general
        FROM Resenas
        WHERE estado = 'habilitada'
    """

    try:
        cursor.execute(query)
        promedio_resenas = cursor.fetchone()

    finally:
        cursor.close()
        conn.close()

    return promedio_resenas


# Obtiene el servicio más solicitado por los clientes.
def obtener_servicio_mas_solicitado():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            s.nombre,
            COUNT(*) AS cantidad
        FROM Servicios_reserva sr
        JOIN Servicios s
            ON sr.servicio_id = s.servicio_id
        GROUP BY s.servicio_id, s.nombre
        ORDER BY cantidad DESC
        LIMIT 1
    """

    try:
        cursor.execute(query)
        servicio_mas_solicitado = cursor.fetchone()

    finally:
        cursor.close()
        conn.close()

    return servicio_mas_solicitado