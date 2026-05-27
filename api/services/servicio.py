from api.database.servicio import *

from api.utils.errors import *
from api.utils.pagination import *

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