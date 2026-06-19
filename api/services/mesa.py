from api.database.mesa import *
from api.utils.errors import *


# Obtiene la cantidad de mesas ocupadas y desocupadas.
def disponibilidad_mesas():

    resultados = obtener_conteo_mesas_db()

    if not resultados:
        raise ValueError("NOT_FOUND")

    conteo = {
        "ocupadas": 0,
        "desocupadas": 0
    }

    for fila in resultados:

        estado = fila["estado"]
        cantidad = fila["cantidad_mesas"]

        if estado == "ocupada":
            conteo["ocupadas"] = cantidad

        elif estado == "desocupada":
            conteo["desocupadas"] = cantidad

    return conteo


# Actualiza la cantidad de mesas de un estado específico.
def actualizar_cantidad_mesas(estado, body):

    if estado not in ["ocupada", "desocupada"]:
        raise ValueError("BAD_REQUEST")

    if "cantidad_mesas" not in body:
        raise ValueError("BAD_REQUEST")

    cantidad = body["cantidad_mesas"]

    if not isinstance(cantidad, int) or cantidad < 0:
        raise ValueError("BAD_REQUEST")

    filas_afectadas = actualizar_cantidad_mesas_db(
        estado,
        cantidad
    )

    if filas_afectadas == 0:
        raise ValueError("NOT_FOUND")

    return True

# Actualiza la capacidad total de mesas del local.
def actualizar_capacidad_local(body):

    if "cantidad_mesas" not in body:
        raise ValueError("BAD_REQUEST")

    nueva_capacidad = body["cantidad_mesas"]

    if not isinstance(nueva_capacidad, int):
        raise ValueError("BAD_REQUEST")

    if nueva_capacidad <= 0:
        raise ValueError("BAD_REQUEST")

    ocupadas = obtener_cantidad_por_estado_db("ocupada")

    if ocupadas is None:
        raise ValueError("NOT_FOUND")

    if nueva_capacidad < ocupadas:
        raise ValueError("BAD_REQUEST")

    nuevas_desocupadas = nueva_capacidad - ocupadas

    actualizar_cantidad_mesas_db(
        "desocupada",
        nuevas_desocupadas
    )

    return True
