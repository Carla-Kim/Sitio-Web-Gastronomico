from ..database.usuario import *
from ..utils.errors import *
from utils.pagination import build_links


# Función para el endpoint de listar usuarios
def obtener_usuarios(base_url, query_params, limit, offset, rol):
    usuarios, total = seleccionar_usuarios(
        limit=limit,
        offset=offset,
        rol=rol
    )

    args_for_links = query_params.copy()

    args_for_links.pop("_limit", None)
    args_for_links.pop("_offset", None)

    links = build_links(
        base_url=base_url,
        query_params=args_for_links,
        limit=limit,
        offset=offset,
        total=total
    )

    response_body = {
        "_links": links,
        "count": total,
        "data": usuarios
    }

    return response_body

# Función para el endpoint de buscar usuario por ID
def obtener_usuario_por_id(id):
    usuario = seleccionar_usuario_por_id(id)

    if not usuario:
        raise ValueError("NOT_FOUND")

    return usuario

# Función para el endpoint de mostrar contraseña por email
def obtener_contrasena_por_email(email):
    contrasena = seleccionar_contrasena_por_email(email)

    if not contrasena:
        raise ValueError("NOT_FOUND")

    return contrasena

# Función para el endpoint de mostrar rol
def obtener_rol_por_email(email):
    rol = seleccionar_rol_por_email(email)

    if not rol:
        raise ValueError("NOT_FOUND")

    return rol