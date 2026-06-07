import mysql.connector
from config import DB_CONFIG, DB_NAME
from .connection import get_connection

def insert_reserva(fecha, email, nombre, apellido, dni, servicio_id, telefono, cantidad_personas, estado):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Reservas (fecha, email, nombre, apellido, DNI, servicio_ID, telefono, cantidad_personas, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (fecha, email, nombre, apellido, dni, servicio_id, telefono, cantidad_personas, estado)
        )
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        conn.rollback()
        if err.errno == 1062:
            return 'duplicado'
        if err.errno == 1452:
            return 'servicio_no_existe'
        raise err
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        cursor.close()
        conn.close()

def update_reserva(id, fecha, email, nombre, apellido, dni, servicio_id, telefono, cantidad_personas, estado):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Reservas SET fecha = %s, email = %s, nombre = %s, apellido = %s, DNI = %s, servicio_ID = %s, telefono = %s, cantidad_personas = %s, estado = %s WHERE reserva_id = %s",
            (fecha, email, nombre, apellido, dni, servicio_id, telefono, cantidad_personas, estado, id)
        )
        conn.commit()
        return cursor.rowcount
    except mysql.connector.Error as err:#Manejo de errores que uso despues en services y r
        conn.rollback()
        if err.errno == 1452:
            return 'servicio_no_existe'
        raise err
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        cursor.close()
        conn.close()

def seleccionar_reservas(limit, offset):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) AS total FROM Reservas")
        total = cursor.fetchone()['total']
        
        query = "SELECT * FROM Reservas ORDER BY reserva_id LIMIT %s OFFSET %s"
        cursor.execute(query, [limit, offset])
        reservas = cursor.fetchall()
        return reservas, total
    finally:
        cursor.close()
        conn.close()

def seleccionar_unica_reserva(id): #Borrar en caso de no ser necesaria utilizar
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM Reservas WHERE reserva_id = %s"
        cursor.execute(query, [id])
        reserva = cursor.fetchone()
        return reserva
    finally:
        cursor.close()
        conn.close()

def seleccionar_reservas_por_estado(estado, limit, offset): #Usamos paginacion también por si son muchas
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT COUNT(*) AS total FROM Reservas WHERE estado = %s"
        cursor.execute(query, [estado])
        total = cursor.fetchone()['total']
        
        query = "SELECT * FROM Reservas WHERE estado = %s ORDER BY reserva_id LIMIT %s OFFSET %s"
        cursor.execute(query, [estado, limit, offset])
        reservas = cursor.fetchall()
        return reservas, total
    finally:
        cursor.close()
        conn.close()

def cambiar_estado_cancelado(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)    
    try:
        query_datos = "SELECT nombre, email, fecha FROM Reservas WHERE reserva_id = %s"
        cursor.execute(query_datos, (id,))
        datos_reserva = cursor.fetchone()

        if not datos_reserva:
            return 0, None

        query_update = "UPDATE Reservas SET estado = 'cancelada' WHERE reserva_id = %s"
        cursor.execute(query_update, (id,))
        conn.commit()
        
        return cursor.rowcount, datos_reserva
    except Exception as e:
        print(f"Error en DB al cancelar: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()

def seleccionar_reservas_por_fecha(fecha, limit, offset):#Misma lógica que la anterior, tal vez optimizable.
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT COUNT(*) AS total FROM Reservas WHERE fecha = %s"
        cursor.execute(query, [fecha])
        total = cursor.fetchone()['total']
        
        query = "SELECT * FROM Reservas WHERE fecha = %s ORDER BY reserva_id LIMIT %s OFFSET %s"
        cursor.execute(query, [fecha, limit, offset])
        reservas = cursor.fetchall()
        return reservas, total
    finally:
        cursor.close()
        conn.close()

def cambiar_estado_finalizado(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)    
    try:
        query = "UPDATE Reservas SET estado = 'finalizada' WHERE reserva_id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Error en DB al finalizar por QR: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()
