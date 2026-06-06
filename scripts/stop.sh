#!/bin/sh
set -e

if [ "$1" = "local" ]; then
    echo "Deteniendo la app local (si está corriendo) y bajando contenedores..."
    pkill -f main_app.py || true
    sudo docker compose down
else
    echo "Bajando servicios con Docker Compose..."
    sudo docker compose down
fi
