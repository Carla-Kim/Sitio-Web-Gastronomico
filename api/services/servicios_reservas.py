from ..database import servicios_reservas as sr
from ..utils.errors import *

# =====================================================
# OBTENER TODOS LOS SERVICIOS POR RESERVA
# Recupera todas las asociaciones entre reservas y servicios.
# =====================================================

def obtener_servicios_reserva():
    servicios = sr.seleccionar_servicios_reserva()

    if not servicios:
        raise ValueError("NOT_FOUND")

    return servicios

# =====================================================
# OBTENER SERVICIOS DE UNA RESERVA
# Recupera los servicios asociados a una reserva específica.
# =====================================================

def obtener_servicios_por_reserva(reserva_id):
    servicios = sr.seleccionar_servicios_por_reserva(reserva_id)

    if not servicios:
        raise ValueError("NOT_FOUND")

    return servicios

# =====================================================
# ASOCIAR SERVICIOS A UNA RESERVA
# Valida los datos recibidos y delega la creación de las asociaciones a la capa de base de datos.
# =====================================================

def asociar_servicios_reserva(reserva_id, body):
    if "servicios_id" not in body:
        raise ValueError("BAD_REQUEST")

    result = sr.insertar_servicios_reserva(
        reserva_id,
        body["servicios_id"]
    )

    if result == "NOT_FOUND":
        raise ValueError("NOT_FOUND")

    if result == "CONFLICT":
        raise ValueError("CONFLICT")

# =====================================================
# ELIMINAR SERVICIOS DE UNA RESERVA
# Elimina todas las asociaciones de servicios vinculadas a una reserva.
# =====================================================

def eliminar_servicios_reserva(reserva_id):
    deleted_rows = sr.eliminar_servicios_reserva_db(reserva_id)

    if deleted_rows == 0:
        raise ValueError("NOT_FOUND")