#!/bin/sh
set -e

# Ir a la raiz del proyecto
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="$PROJECT_ROOT"

# Detectar python del venv
PYTHON=".venv/bin/python3"
if [ ! -x "$PYTHON" ]; then
    PYTHON="python"
fi

if [ "$1" = "local" ]; then

    echo "Levantando MySQL..."
    sudo docker compose up -d db

    export DB_HOST=127.0.0.1
    export DB_USER=flask_user
    export DB_PASSWORD=flask_password
    export DB_NAME=gastronomia_db

    echo "Esperando MySQL..."

until "$PYTHON" -c 'import mysql.connector
try:
    mysql.connector.connect(
        host="127.0.0.1",
        user="flask_user",
        password="flask_password",
        port=3306
    ).close()
except Exception:
    import sys
    sys.exit(1)
' 2>/dev/null
    do
        echo "MySQL se está inicializando..."
        sleep 2
    done

    echo "MySQL listo."

    echo "Ejecutando init..."

    "$PYTHON" data/init_db.py

    echo "Iniciando app..."

    "$PYTHON" main_app.py

else
    sudo docker compose up -d --build
    echo "Servicios iniciados."
fi