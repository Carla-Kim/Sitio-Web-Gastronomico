from api.database.servicio import *
from api.utils.errors import *
from api.utils.pagination import *

#Ver todos los servicios 
def ver_servicios(base_url, query_params, limit, offset):
    servicios, total = obtener_servicios(limit, offset)
    
    if total == 0:
        raise ValueError("NOT_FOUND")
    
    args_for_links = query_params.copy()
    args_for_links.pop("_limit", None)
    args_for_links.pop("_offset", None)

    links = build_links(base_url, args_for_links, limit, offset, total)

    response_body = {
        "_links" : links,
        "count" : total,
        "data" : servicios 
    }

    return response_body

#Ver un servicio por estado.
def ver_servicios_estado(estado):

    if estado not in ["habilitado", "deshabilitado"]:
        raise ValueError("BAD_REQUEST")

    servicios = obtener_servicios_estado(estado)

    if len(servicios) == 0:
        raise ValueError("NOT_FOUND")

    return servicios

#Ver un servicio por ID
def ver_servicio_id(servicio_id):
    servicio = obtener_servicio_id(servicio_id)
    
    if servicio is None:
        raise ValueError("NOT_FOUND")
    
    return servicio

#crear un nuevo servicio
def crear_servicio(body):
    required_field = ["nombre"]

    if required_field[0] not in body:
        raise ValueError("BAD_REQUEST")
    
    validacion = verificacion_servicio(body) 

    if validacion is None:
        create = insertar_servicio(body)
        return {
            "servicio": create,
            "message": "Servicio creado exitosamente"
        }
    else:
        raise ValueError("CONFLICT")

#Actualizar nommbre
def actualizar_nombre_servicio(servicio_id, body):

    if "nombre" not in body:
        raise ValueError("BAD_REQUEST")

    body["nombre"] = body["nombre"].strip()

    if not body["nombre"]:
        raise ValueError("BAD_REQUEST")

    servicio = obtener_servicio_id(servicio_id)

    if servicio is None:
        raise ValueError("NOT_FOUND")

    existe_nombre = verificacion_servicio(body)

    if existe_nombre and existe_nombre["servicio_id"] != servicio_id:
        raise ValueError("CONFLICT")

    actualizar_nombre_servicio_db(servicio_id, body["nombre"])

    return True
    
#actualizar estado.
def actualizar_estado_servicio(servicio_id, body):

    if "estado" not in body:
        raise ValueError("BAD_REQUEST")

    if body["estado"] not in ["habilitado", "deshabilitado"]:
        raise ValueError("BAD_REQUEST")

    servicio = obtener_servicio_id(servicio_id)

    if servicio is None:
        raise ValueError("NOT_FOUND")

    actualizar_estado_servicio_db(
        servicio_id,
        body["estado"]
    )

    return True
        

