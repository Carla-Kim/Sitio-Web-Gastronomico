from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from api import app as backend
from web import app as frontend

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(
    frontend.wsgi_app,
    {
        '/api': backend.wsgi_app
    }
)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
