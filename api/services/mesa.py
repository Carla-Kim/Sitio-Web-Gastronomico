from api.database.mesa import *
from api.utils.errors import *


#cantidad de mesas segun su estado (ocupada/desocupada)
def disponibilidad_mesas():
    resultados = obtener_conteo_mesas_db()
    if not resultados:
        raise ValueError("NOT_FOUND")

    conteo = {
        "desocupadas": 0,
        "ocupadas": 0
    }
    
    for fila in resultados:
        estado = fila[0]     
        cantidad = fila[1]   
        
        if estado == 'desocupada':
            conteo["desocupadas"] = cantidad
        elif estado == 'ocupada':
            conteo["ocupadas"] = cantidad

    return conteo



#actualizar estado de una mesa (ocupado/desocupado)
def actualizar_Estado(mesa_id, body):
    
    if "estado" not in body or not body["estado"]:
        raise ValueError("BAD_REQUEST")
    
    estado_valor = body["estado"]
    if estado_valor not in ["ocupada", "desocupada"]:
        raise ValueError("BAD_REQUEST")
    
    estado = estado_actualizado_db(mesa_id, estado_valor)

    if estado == 0:
        raise ValueError("NOT_FOUND")
    
    return True

def crear_nueva_mesa():
    nuevo_id = crear_mesa_db('desocupada', 2)
    return nuevo_id

def eliminar_mesa(mesa_id):
    filas_afectadas = borrar_mesa_db(mesa_id)
    if filas_afectadas == 0:
        raise ValueError("NOT_FOUND")
    return True