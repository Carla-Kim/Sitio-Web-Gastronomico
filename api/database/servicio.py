from .connection import get_connection

#Obtener servicios con paginacion desde la db.
def obtener_servicios(limit, offset):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        sql_count = "SELECT COUNT(*) as count FROM Servicios"
        cursor.execute(sql_count)
        total = cursor.fetchone()["count"]

        sql_elems = "SELECT * FROM Servicios ORDER BY servicio_id LIMIT %s OFFSET %s"
        cursor.execute(sql_elems, [limit, offset])
        servicios = cursor.fetchall()

        return servicios, total
    
    finally:
        cursor.close()
        conn.close()

#Obtener un servicio por estado desde la db.
def obtener_servicios_estado(estado):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT *
            FROM Servicios
            WHERE estado = %s
            ORDER BY servicio_id
        """

        cursor.execute(query, [estado])

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

#Obtener un servicio por ID desde la db.
def obtener_servicio_id(servicio_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM Servicios WHERE servicio_id = %s"
        cursor.execute(query, [servicio_id])
        servicio = cursor.fetchone()
        return servicio
    
    finally:
        cursor.close()
        conn.close()

#verificacion de un servicio antes de su creacion.
def verificacion_servicio(body):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM Servicios WHERE nombre = %s"
        cursor.execute(query, [body["nombre"]])
        
        return cursor.fetchone()
    
    finally:
        cursor.close()
        conn.close()

#Insertar un nuevo servicio en la db.
def insertar_servicio(body):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = "INSERT INTO Servicios (nombre) VALUES (%s)"
        cursor.execute(query, [body["nombre"]])
        conn.commit()

        return cursor.lastrowid
    
    finally:
        cursor.close()
        conn.close()


#Actualizar un servicio por ID en la db.
def servicio_actualizado_db(servicio_id, body):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = "UPDATE Servicios SET nombre = %s WHERE servicio_id = %s"
        cursor.execute(query, [body["nombre"], servicio_id])
        conn.commit()

        return cursor.rowcount
    
    finally:
        cursor.close()
        conn.close()

#Cambia el estado de un servicio de la db.
def actualizar_estado_servicio(servicio_id, estado):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
            UPDATE Servicios
            SET estado = %s
            WHERE servicio_id = %s
        """

        cursor.execute(query, [estado, servicio_id])
        conn.commit()

        return cursor.rowcount

    finally:
        cursor.close()
        conn.close()