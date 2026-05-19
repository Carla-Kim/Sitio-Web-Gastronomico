import mysql.connector
from config import DB_CONFIG, DB_NAME

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(f"SHOW DATABASES LIKE '{DB_NAME}'")
    initialized = cursor.fetchone()

    with open("data/init_db.sql", "r", encoding="utf-8") as f:
        sql_init = f.read()

    for line in sql_init.split(';'):
        if line.strip():
            cursor.execute(line)

    conn.commit()
    print("Base de datos creada.")

except mysql.connector.Error as err:
    print(f"Error de MySQL: {err}")

except FileNotFoundError:
    print("Archivo data/init_db.sql no encontrado.")

finally:
    cursor.close()
    conn.close()
