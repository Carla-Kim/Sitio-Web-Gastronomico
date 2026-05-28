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