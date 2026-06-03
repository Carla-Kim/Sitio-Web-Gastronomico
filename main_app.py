from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from api.app import app as backend
from web.app import app as frontend

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(
    frontend.wsgi_app,
    {
        '/api': backend.wsgi_app
    }
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
# el host 0.0.0.0 sirve para que la app sea accesible desde fuera del contenedor Docker (para postman), y el puerto 5000 es el puerto por defecto de Flask. El debug=True es útil durante el desarrollo para ver errores detallados, pero debería ser False en producción