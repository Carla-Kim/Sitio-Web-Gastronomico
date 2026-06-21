# Sitio-Web-Gastronomico
Proyecto integrador - Introducción al Desarrollo de Software 1C2026 (Curso Lanzillotta)

## Integrantes:
- Carla Sabrina, Kim, cskim@fi.uba.ar, 115704;
- Florencia, Avila, flavila@fi.uba.ar, 114386;
- John, Lima, jlima@fi.uba.ar, 115622;
- Kevin Ezequiel, La Rocca, klarocca@fi.uba.ar, 115834;
- Luis, Pérez, lperezj@fi.uba.ar, 115066;
- Matías Agustín, Cáceres, macaceres@fi.uba.ar, 101883;
- Neithan, Larez, nlarez@fi.uba.ar, 114904;
- Nicolás Agustín, West, nwest@fi.uba.ar, 115416.

## Stack Tecnológico
- **Core**: Flask, Werkzeug.
- **Base de Datos**: MySQL (via `mysql-connector-python`).
- **Comunicación**: `flask-cors` para integración Frontend-Backend.
- **Notificaciones**: `flask-mailman` para el envío de correos automatizados.
- **Utilidades**: `qrcode` para menús digitales.
- **Configuración**: `python-dotenv` para gestión segura de variables de entorno.
- **Frontend**: Jinja2 para renderizado dinámico.

## Estructura del Proyecto
La arquitectura se organiza de la siguiente manera:
- `api/`: Backend completo.
  - `routes/`: Endpoints de la API.
  - `services/`: Lógica de negocio y reglas de validación.
  - `database/`: Gestión de consultas SQL y conexión.
  - `utils/`: Herramientas transversales (QR, paginación).
- `data/`: Scripts para inicialización de la base de datos.
- `web/`: Frontend (Templates y archivos estáticos).
- `scripts/`: Automatización del ciclo de vida del proyecto.

## Inicio rápido

Las tareas principales ya están automatizadas con scripts en `scripts/`.

### 1) Configuración inicial
#### Para descargar (clonar) tu repositorio

```bash
git clone <url_del_repo>
cd nombre-de-tu-carpeta
```

#### Configurar el .env

El proyecto usa estas variables de entorno para el envío de correo:

- `EMAIL_USER` → cuenta de email remitente
- `EMAIL_APP_PASSWORD` → contraseña SMTP / password de aplicación

La idea es crear esto desde gmail. Van a cuenta, verificación en 2 pasos
bajan hasta abajo de todo y les aparece contraseña de aplicaciones. Les da
la de 16 digitos. Apliquen todo en el .env y borren todos los espacios.

Crea un archivo `.env` en la raíz del proyecto con:

```env
SUPABASE_URL=https://uepxnfxlzaljovgxobqd.supabase.co/
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVlcHhuZnhsemFsam92Z3hvYnFkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODEzMDQyMzYsImV4cCI6MjA5Njg4MDIzNn0.xvNdq5S7JwUDGBi4Ftm3wRRWY9em0jwQX2_Xe3EH1HQ
SUPABASE_BUCKET=productos
EMAIL_USER=tu-email@gmail.com
EMAIL_APP_PASSWORD=tu-app-password
```

#### Configuración del entorno
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Con Docker (todo el proyecto)

```bash
./scripts/start.sh
```

Parar todo:

```bash
./scripts/stop.sh
sudo systemctl stop mysql
```

Si necesitás borrar los datos y volver a recrear la base de datos:

```bash
./scripts/stop.sh local
sudo systemctl stop mysql
./scripts/start.sh
```

### 3) Modo mixto / desarrollo local

Este modo levanta solo la base de datos en Docker y arranca la app local con Python.

```bash
./scripts/start.sh local
```

Para detener el modo local:

```bash
./scripts/stop.sh local
sudo systemctl stop mysql
```

### 3) Comandos manuales
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d db
.venv/bin/python3 data/init_db.py
.venv/bin/python3 main_app.py

```

```bash
# desde la raíz del proyecto
sudo docker compose up -d --build
```

Para parar:

```bash
sudo docker compose down
sudo systemctl stop mysql
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
