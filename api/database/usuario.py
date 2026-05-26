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

# crear usuario
def insertar_usuario(body):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        check_query = """
            SELECT usuario_id
            FROM Usuarios
            WHERE usuario = %s
            OR email = %s
        """

        cursor.execute(
            check_query,
            [
                body["usuario"],
                body["email"]
            ]
        )

        existing_user = cursor.fetchone()

        if existing_user:
            return "CONFLICT"

        insert_query = """
            INSERT INTO Usuarios (
                usuario,
                contrasena,
                email,
                nombre,
                apellido,
                rol
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = [
            body["usuario"],
            body["contrasena"],
            body["email"],
            body["nombre"],
            body["apellido"],
            body["rol"]
        ]

        cursor.execute(insert_query, values)

        conn.commit()

        return cursor.lastrowid

    finally:
        cursor.close()
        conn.close()

# modificar usuario
def actualizar_usuario_db(id, body):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
            UPDATE Usuarios
            SET
                usuario = %s,
                contrasena = %s,
                email = %s,
                nombre = %s,
                apellido = %s,
                rol = %s
            WHERE usuario_id = %s
        """

        values = [
            body["usuario"],
            body["contrasena"],
            body["email"],
            body["nombre"],
            body["apellido"],
            body["rol"],
            id
        ]

        cursor.execute(query, values)

        conn.commit()

        return cursor.rowcount

    finally:
        cursor.close()
        conn.close()

# modificar parcialmente usuario
def actualizar_usuario_parcial_db(id, body):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        fields = []
        values = []

        if "email" in body:
            fields.append("email = %s")
            values.append(body["email"])

        if "contrasena" in body:
            fields.append("contrasena = %s")
            values.append(body["contrasena"])

        query = f"""
            UPDATE Usuarios
            SET {", ".join(fields)}
            WHERE usuario_id = %s
        """

        values.append(id)

        cursor.execute(query, values)

        conn.commit()

        return cursor.rowcount

    finally:
        cursor.close()
        conn.close()

# borrar usuario
def eliminar_usuario_db(id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
            DELETE FROM Usuarios
            WHERE usuario_id = %s
        """

        cursor.execute(query, [id])

        conn.commit()

        return cursor.rowcount

    finally:
        cursor.close()
        conn.close()