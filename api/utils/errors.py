def ReturnErrors(status_code):
    """Devuelve un payload de error estandarizado según el código HTTP.

    Args:
        status_code (int): Código HTTP (ej. 400, 404, 409, 415, 500)

    Returns:
        dict: Estructura {'errors': [{...}]}
    """
    mapping = {
        400: {
            "code": "BAD_REQUEST",
            "description": "Solicitud inválida. Verifique los parámetros o el cuerpo de la petición.",
            "level": "error",
            "message": "Solicitud inválida"
        },
        401: {
            "code": "UNAUTHORIZED",
            "description": "Acceso denegado. Credenciales inválidas o inexistentes.",
            "level": "info",
            "message": "Credenciales inválidas"
        },
        404: {
            "code": "NOT_FOUND",
            "description": "El recurso solicitado no existe.",
            "level": "error",
            "message": "Recurso no encontrado"
        },
        409: {
            "code": "CONFLICT",
            "description": "Conflicto al procesar la solicitud (por ejemplo, recurso duplicado).",
            "level": "error",
            "message": "Conflicto"
        },
        415: {
            "code": "UNSUPPORTED_MEDIA_TYPE",
            "description": "Tipo de contenido no soportado. Use 'application/json'.",
            "level": "error",
            "message": "Tipo de contenido no soportado"
        },
        500: {
            "code": "INTERNAL_SERVER_ERROR",
            "description": "Ocurrió un fallo inesperado. Por favor, contacta al soporte técnico.",
            "level": "critical",
            "message": "Error interno del servidor"
        }
    }

    err = mapping.get(status_code, {
        "code": "ERROR",
        "description": "Error.",
        "level": "error",
        "message": "Error"
    })

    return {"errors": [err]}
