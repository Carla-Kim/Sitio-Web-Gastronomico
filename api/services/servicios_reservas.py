from ..database.servicios_reservas import *
from ..utils.errors import *


def obtener_servicios_reserva():
    servicios = seleccionar_servicios_reserva()

    if not servicios:
        raise ValueError("NOT_FOUND")

    return servicios


def obtener_servicios_por_reserva(reserva_id):
    servicios = seleccionar_servicios_por_reserva(reserva_id)

    if not servicios:
        raise ValueError("NOT_FOUND")

    return servicios


def asociar_servicios_reserva(reserva_id, body):
    if "servicios_id" not in body:
        raise ValueError("BAD_REQUEST")

    result = insertar_servicios_reserva(
        reserva_id,
        body["servicios_id"]
    )

    if result == "NOT_FOUND":
        raise ValueError("NOT_FOUND")

    if result == "CONFLICT":
        raise ValueError("CONFLICT")


def eliminar_servicios_reserva(reserva_id):
    deleted_rows = eliminar_servicios_reserva_db(reserva_id)

    if deleted_rows == 0:
        raise ValueError("NOT_FOUND")