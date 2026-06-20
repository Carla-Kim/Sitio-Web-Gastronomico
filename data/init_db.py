import mysql.connector
from api.database.config import DB_CONFIG

ADMIN = {
    "nombre": "Administrador",
    "apellido": "Sistema",
    "nombre_usuario": "admin",
    "email": "admin@admin.com",
    "contrasena": "admin123",
    "rol": "admin"
}


def ejecutar_sql(cursor, archivo):
    with open(archivo, "r", encoding="utf-8") as f:
        sql = f.read()

    # ✔ forma correcta para mysql-connector
    for result in cursor.execute(sql, multi=True):
        pass


def crear_instalacion_demo(cursor):
    ejecutar_sql(cursor, "data/demo_data.sql")


def crear_instalacion_vacia(cursor):
    total_mesas = int(input("¿Cuántas mesas tiene el local?: "))

    cursor.execute("""
        INSERT INTO Usuarios
        (nombre, apellido, nombre_usuario, email, contrasena, rol)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        ADMIN["nombre"],
        ADMIN["apellido"],
        ADMIN["nombre_usuario"],
        ADMIN["email"],
        ADMIN["contrasena"],
        ADMIN["rol"]
    ))

    cursor.execute("""
        INSERT INTO Mesas (estado, cantidad_mesas)
        VALUES ('ocupada', 0)
    """)

    cursor.execute("""
        INSERT INTO Mesas (estado, cantidad_mesas)
        VALUES ('desocupada', %s)
    """, (total_mesas,))


def main():
    print("\n====================================")
    print("Inicialización del Sistema")
    print("====================================")
    print("1) Proyecto vacío")
    print("2) Proyecto demo")
    print("====================================")

    opcion = input("Seleccione una opción: ")

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        cursor.execute("DROP DATABASE IF EXISTS gastronomia_db")

        ejecutar_sql(cursor, "data/schema.sql")

        cursor.execute("USE gastronomia_db")

        if opcion == "1":
            crear_instalacion_vacia(cursor)

        elif opcion == "2":
            crear_instalacion_demo(cursor)

        else:
            raise ValueError("Opción inválida")

        conn.commit()

        print("\nInicialización completada.\n")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()