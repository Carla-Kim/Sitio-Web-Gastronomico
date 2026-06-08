#!/bin/sh
set -e

#Si se configuró DB_HOST entonces asumimos que hay una base de datos a la cual conectarse, esperamos a que la base de datos esté disponible antes de iniciar la app.

if [ -n "$DB_HOST" ]; then
    echo "Esperando a la base de datos en $DB_HOST:$DB_PORT..."
    until python - <<PYTHON #esta linea significa "ejecuta el siguiente código Python hasta que funcione"

# este código Python intenta conectarse a la base de datos usando las variables de entorno. Si la conexión falla, se lanza una excepción y el script vuelve a intentar después de dormir 1 segundo.

import os
import mysql.connector
try:
    mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=int(os.getenv('DB_PORT', '3306')),
        database=os.getenv('DB_NAME')
    ).close()
    print('DB disponible')
except Exception as e:
    raise SystemExit(1)

PYTHON
    do
        sleep 1
    done
fi

#inicializa la base de datos con tablas y datos si es necesario. Luego arranca la app
python data/init_db.py
exec python main_app.py
