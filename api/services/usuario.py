from ..database import usuario as us
from api.utils.errors import ReturnErrors
from api.utils.pagination import build_links

def obtener_usuarios(base_url, query_params, limit, offset, rol):
    usuarios, total = us.seleccionar_usuarios(
        limit=limit,
        offset=offset,
        rol=rol
    )

    args_for_links = query_params.copy()
    
    args_for_links.pop("limit", None)
    args_for_links.pop("offset", None)

    links = build_links(
        base_url=base_url,
        args=args_for_links,
        limit=limit,
        offset=offset,
        count=total
    )

    response_body = {
        "_links": links,
        "count": total,
        "data": usuarios
    }

    return response_body

# Función para el endpoint de buscar usuario por ID
def obtener_usuario_por_id(id):
    usuario = us.seleccionar_usuario_por_id(id)

    if not usuario:
        raise ValueError("NOT_FOUND")

    return usuario

# Función para el endpoint de mostrar contraseña por email
def obtener_contrasena_por_email(email):
    contrasena = us.seleccionar_contrasena_por_email(email)

    if not contrasena:
        raise ValueError("NOT_FOUND")

    return contrasena

# Función para el endpoint de mostrar rol
def obtener_rol_por_email(email):
    rol = us.seleccionar_rol_por_email(email)

    if not rol:
        raise ValueError("NOT_FOUND")

    return rol

# Función para el endpoint de crear usuario
def crear_nuevo_usuario(body):
    required_fields = [
        "nombre_usuario",  
        "contrasena",
        "email",
        "nombre",
        "apellido",
        "rol"
    ]

    for field in required_fields:
        if field not in body:
            raise ValueError("BAD_REQUEST")

    usuario_id = us.insertar_usuario(body)

    if usuario_id == "CONFLICT":
        raise ValueError("CONFLICT")

    return {
        "usuario_id": usuario_id,
        "message": "Usuario creado correctamente"
    }

# Función para el endpoint de modificar usuario
def actualizar_usuario(id, body):
    required_fields = [
        "nombre_usuario",
        "contrasena",
        "email",
        "nombre",
        "apellido",
        "rol"
    ]

    for field in required_fields:
        if field not in body:
            raise ValueError("BAD_REQUEST")

    updated_rows = us.actualizar_usuario_db(id, body)

    if updated_rows == 0:
        raise ValueError("NOT_FOUND")
        
    return True
    
# Función para el endpoint de modificar parcialmente usuario
def actualizar_usuario_parcial(id, body):
    allowed_fields = ["email", "contrasena"]

    if not any(field in body for field in allowed_fields):
        raise ValueError("BAD_REQUEST")

    updated_rows =us.actualizar_usuario_parcial_db(id, body)

    if updated_rows == 0:
        raise ValueError("NOT_FOUND")
    
# Función para el endpoint de borrar usuario
def eliminar_usuario(id):
    deleted_rows = us.eliminar_usuario_db(id)

    if deleted_rows == 0:
        raise ValueError("NOT_FOUND")