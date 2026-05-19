ERROR_CATALOG = {
    400: {
        "code": "BAD_REQUEST",
        "message": "La solicitud es inválida",
        "level": "error",
        "description": "Los datos enviados no cumplen con los requisitos del sistema o el esquema."
    },
    404: {
        "code": "NOT_FOUND",
        "message": "Recurso no encontrado",
        "level": "warning",
        "description": "El elemento solicitado no existe en la base de datos."
    },
    409: {
        "code": "CONFLICT",
        "message": "Conflicto en la solicitud",
        "level": "error",
        "description": "La operación no se pudo completar porque el recurso ya existe o genera un conflicto de integridad."
    },
    415: {
        "code": "UNSUPPORTED_MEDIA_TYPE",
        "message": "Tipo de medio no soportado",
        "level": "error",
        "description": "El servidor no puede procesar el formato de los datos enviados. Asegúrese de usar 'application/json'."
    },
    500: {
        "code": "INTERNAL_SERVER_ERROR",
        "message": "Error interno del servidor",
        "level": "critical",
        "description": "Ocurrió un fallo inesperado. Por favor, contacta al soporte técnico."
    }
}

def ReturnErrors(*status_codes):
    errors = []

    for code in status_codes:
        errors.append(ERROR_CATALOG.get(code, ERROR_CATALOG[500]))
    
    return {
        "errors": errors
    }
