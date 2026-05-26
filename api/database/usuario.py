from database.connection import *


# listado de usuarios
def seleccionar_usuarios(limit, offset, rol=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        filters = []
        values = []

        if rol:
            filters.append("rol = %s")
            values.append(rol)

        where_clause = ""

        if filters:
            where_clause = "WHERE " + " AND ".join(filters)

        count_query = f"""
            SELECT COUNT(*) AS total
            FROM Usuarios
            {where_clause}
        """

        cursor.execute(count_query, values)

        total = cursor.fetchone()["total"]

        query = f"""
            SELECT
                usuario,
                email,
                nombre,
                apellido
            FROM Usuarios
            {where_clause}
            ORDER BY usuario_id
            LIMIT %s OFFSET %s
        """

        cursor.execute(
            query,
            values + [limit, offset]
        )

        usuarios = cursor.fetchall()

        return usuarios, total

    finally:
        cursor.close()
        conn.close()

# buscar usuario por ID
def seleccionar_usuario_por_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT
                usuario_id,
                usuario,
                email,
                nombre,
                apellido,
                rol
            FROM Usuarios
            WHERE usuario_id = %s
        """

        cursor.execute(query, [id])

        usuario = cursor.fetchone()

        return usuario

    finally:
        cursor.close()
        conn.close()

# mostrar contraseña por email
def seleccionar_contrasena_por_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT contrasena
            FROM Usuarios
            WHERE email = %s
        """

        cursor.execute(query, [email])

        contrasena = cursor.fetchone()

        return contrasena

    finally:
        cursor.close()
        conn.close()

# mostrar rol por email
def seleccionar_rol_por_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT rol
            FROM Usuarios
            WHERE email = %s
        """

        cursor.execute(query, [email])

        rol = cursor.fetchone()

        return rol

    finally:
        cursor.close()
        conn.close()