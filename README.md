# Sitio-Web-Gastronomico
Proyecto integrador - Introducción al Desarrollo de Software 1C2026 (Curso Lanzillotta)

## Integrantes:
- Carla Sabrina, Kim, cskim@fi.uba.ar, 115704;
- Florencia, Avila, flavila@fi.uba.ar, 114386;
- John, Lima, jlima@fi.uba.ar, 115622;
- Kevin Ezequiel, La Rocca, klarocca@fi.uba.ar, 115834;
- Luis, Pérez, lperezj@fi.uba.ar, 115066;
- Matías Agustín Cáceres, macaceres@fi.uba.ar, 101883;
- Neithan, Larez, nlarez@fi.uba.ar, 114904;
- Nicolás Agustín, West, nwest@fi.uba.ar, 115416.

## Inicio rápido

Las tareas principales ya están automatizadas con scripts en `scripts/`.

### 1) Con Docker (todo el proyecto)

```bash
./scripts/start.sh
```

Parar todo:

```bash
./scripts/stop.sh
```

Si necesitás borrar los datos y volver a recrear la base de datos:

```bash
sudo docker compose down -v
./scripts/start.sh
```

### 2) Modo mixto / desarrollo local

Este modo levanta solo la base de datos en Docker y arranca la app local con Python.

```bash
./scripts/start.sh local
```

Para detener el modo local:

```bash
./scripts/stop.sh local
```

### 3) Comandos manuales

```bash
# desde la raíz del proyecto
sudo docker compose up -d --build
```

Para parar:

```bash
sudo docker compose down
```

Modo manual:

```bash
docker compose up -d db # esto lo que hace es que
source .venv/bin/activate
.venv/bin/python3 data/init_db.py
.venv/bin/python3 main_app.py
```

## Endpoints (ejemplos para Postman)

Base URL: `http://localhost:5000/api`

- Listar usuarios: `GET /api/usuarios`
- Obtener usuario: `GET /api/usuarios/{id}`
- Crear usuario: `POST /api/usuarios` (JSON)

```json
{
	"nombre": "Juan",
	"apellido": "Pérez",
	"nombre_usuario": "juanp",
	"email": "juan@example.com",
	"contrasena": "secreto",
	"rol": "cliente"
}
```