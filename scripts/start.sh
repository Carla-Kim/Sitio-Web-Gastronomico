#!/bin/sh
set -e

PYTHON=".venv/bin/python3"
if [ ! -x "$PYTHON" ]; then
    PYTHON="python3"
fi

if [ "$1" = "local" ]; then
    echo "Iniciando DB en Docker (solo db) y arrancando la app localmente..."
    sudo docker compose up -d db

    echo "Esperar brevemente para que MySQL arranque..."
    sleep 5

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
