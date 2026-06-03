from .connection import get_connection

#Conteo de mesas por estado (ocupada/desocupada)
def obtener_conteo_mesas_db():
    conn = get_connection()
    cursor = conn.cursor() 
    try:
        query = """
            SELECT estado, COUNT(*) as cantidad 
            FROM Mesas 
            GROUP BY estado
        """
        cursor.execute(query)
        return cursor.fetchall() 
    
    finally:
        cursor.close()
        conn.close()


#Actualizar estado de una mesa (ocupada/desocupada)
def estado_actualizado_db(mesa_id, nuevo_estado):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "UPDATE Mesas SET estado = %s WHERE mesa_id = %s"
        cursor.execute(query, [nuevo_estado, mesa_id])
        conn.commit()
        return cursor.rowcount  
    finally:
        cursor.close()
        conn.close()

def crear_mesa_db(estado_inicial, cantidad_personas):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO Mesas (estado, cantidad_personas) VALUES (%s, %s)"
        cursor.execute(query, (estado_inicial, cantidad_personas))
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()

def borrar_mesa_db(mesa_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Mesas WHERE mesa_id = %s", (mesa_id,))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()
