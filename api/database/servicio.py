from api.database.connection import *

#Obtener servicios con paginacion desde la db
def obtener_servicios(limit, offset):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        sql_count = "SELECT COUNT(*) as count FROM servicios"
        cursor.execute(sql_count)
        total = cursor.fetchone()["count"]

        sql_elems = "SELECT * FROM servicios ORDER BY servicios_id LIMIT %s OFFSET %s"
        cursor.execute(sql_elems, [limit, offset])
        servicios = cursor.fetchall()

        return servicios, total
    
    finally:
        cursor.close()
        conn.close()


#Obtener un servicio por ID desde la db
def obtener_servicio_id(servicio_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM servicios WHERE servicios_id = %s"
        cursor.execute(query, [servicio_id])
        servicio = cursor.fetchone()
        return servicio
    
    finally:
        cursor.close()
        conn.close()


#verificacion de un servicio antes de su creacion
def verificacion_servicio(body):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT * FROM servicios WHERE nombre = %s"
        cursor.execute(query, [body["nombre"]])
        
        return cursor.fetchone()
    
    finally:
        cursor.close()
        conn.close()

#Insertar un nuevo servicio en la db
def insertar_servicio(body):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = "INSERT INTO servicios (nombre) VALUES (%s)"
        cursor.execute(query, [body["nombre"]])
        conn.commit()

        return cursor.lastrowid
    
    finally:
        cursor.close()
        conn.close()

#verificacion de un servicio por ID antes de su eliminacion
def verificacion_servicio_id(servicio_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT * FROM servicios WHERE servicios_id = %s"
        cursor.execute(query, [servicio_id])
        
        return cursor.fetchone()
    
    finally:
        cursor.close()
        conn.close()

#Eliminar servicio por ID de la db
def servicio_eliminado(servicio_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = "DELETE FROM servicios WHERE servicios_id = %s"
        cursor.execute(query, [servicio_id])
        conn.commit()
    
    finally:
        cursor.close()
        conn.close()