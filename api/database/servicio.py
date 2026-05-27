from api.database.connection import *

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
