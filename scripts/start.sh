#!/bin/sh
set -e

PYTHON=".venv/bin/python3"
if [ ! -x "$PYTHON" ]; then
    PYTHON="python"
fi

if [ "$1" = "local" ]; then
    echo "Iniciando DB en Docker (solo db) y arrancando la app localmente..."
    sudo docker compose up -d db

    echo "Usando Python: $PYTHON"
    export DB_HOST=127.0.0.1
    export DB_USER=flask_user
    export DB_PASSWORD=flask_password
    export DB_NAME=gastronomia_db

    echo "Esperando a que MySQL acepte conexiones en $DB_HOST:3306..."
    timeout=30
    count=0
    until "$PYTHON" -c 'import mysql.connector; mysql.connector.connect(host="127.0.0.1", user="flask_user", password="flask_password", port=3306).close()' >/dev/null 2>&1; do
        count=$((count + 1))
        if [ "$count" -ge "$timeout" ]; then
            echo ""
            echo "No se pudo conectar a MySQL después de $timeout segundos."
            echo "Revisa que Docker esté corriendo y el contenedor db esté listo."
            exit 1
        fi
        echo -n "."
        sleep 1
    done
    echo ""
    echo "MySQL está listo."

    echo "Inicializando base de datos..."
    if ! "$PYTHON" data/init_db.py; then
        echo ""
        echo "No se pudo inicializar la base de datos automáticamente."
        echo "Ejecuta manualmente:"
        echo "  $PYTHON data/init_db.py"
        echo "Luego vuelve a ejecutar ./scripts/start.sh local"
        exit 1
    fi

    echo "Arrancando la app localmente en primer plano..."
    "$PYTHON" main_app.py
else
    echo "Construyendo y arrancando todos los servicios con Docker Compose..."
    sudo docker compose up -d --build
    echo "Para ver logs: docker compose logs -f"
fi
