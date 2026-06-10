from .connection import get_connection
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
                usuario_id,
                nombre_usuario,
                email,
                nombre,
                apellido,
                rol
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
                nombre_usuario,
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

def actualizar_usuario_db(id, body):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
            UPDATE Usuarios
            SET
                nombre_usuario = %s,
                contrasena = %s,
                email = %s,
                nombre = %s,
                apellido = %s,
                rol = %s
            WHERE usuario_id = %s
        """

        values = [
            body["nombre_usuario"],
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
            WHERE nombre_usuario = %s
            OR email = %s
        """

        cursor.execute(
            check_query,
            [
                body["nombre_usuario"],
                body["email"]
            ]
        )

        existing_user = cursor.fetchone()

        if existing_user:
            return "CONFLICT"

        insert_query = """
            INSERT INTO Usuarios (
                nombre,
                apellido,
                nombre_usuario,
                email,
                contrasena,
                rol
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = [
            body["nombre"],
            body["apellido"],
            body["nombre_usuario"],
            body["email"],
            body["contrasena"],
            body["rol"]
        ]

        cursor.execute(insert_query, values)
        conn.commit()

        return cursor.lastrowid

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

def obtener_usuario_por_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT usuario_id, nombre, apellido, nombre_usuario, email, rol FROM Usuarios WHERE email = %s"
        cursor.execute(query, (email,))
        return cursor.fetchone()
    except Exception as err:
        raise err
    finally:
        cursor.close()
        conn.close()

def obtener_usuarios_por_rol_paginado(rol, limit=10, offset=0):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        sql_count = "SELECT COUNT(*) as total FROM Usuarios WHERE rol = %s"
        cursor.execute(sql_count, (rol,))
        res_count = cursor.fetchone()
        
        total_elementos = res_count["total"] if res_count else 0

        sql_elems = """
            SELECT usuario_id, nombre, apellido, nombre_usuario, email, rol 
            FROM Usuarios 
            WHERE rol = %s 
            LIMIT %s OFFSET %s
        """
        params_elems = (rol, int(limit), int(offset))
        cursor.execute(sql_elems, params_elems)
        rows = cursor.fetchall()

        return {
            "data": rows, 
            "count": total_elementos
        }
    except Exception as err:
        raise err
    finally:
        cursor.close()
        conn.close()

def seleccionar_usuario_id_desde_login(body):
    email = body.get('email')
    contrasena = body.get('contrasena')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT usuario_id
            FROM Usuarios
            WHERE email = %s
            AND contrasena = %s
        """

        cursor.execute(query, (email, contrasena))
        usuario_id = cursor.fetchone()

    finally:
        cursor.close()
        conn.close()

    return usuario_id
