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

    links = build_links(base_url, args_for_links, offset, limit, total)

    response_body = {
        "_links" : links,
        "count" : total,
        "data" : servicios 
    }

    return response_body

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

#Actualizar un servicio por ID


#Eliminar servicio por ID
def eliminar_servicio_id(servicio_id):
    
    delete = servicio_eliminado(servicio_id)

    if delete == 0:
        raise ValueError("NOT_FOUND")
        

