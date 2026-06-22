import os
import sys
import requests
from functools import wraps
from api.app import app as api_app
from api.utils.pagination import build_links
from api.utils.auth import login_requerido
from api.utils.auth import admin_requerido
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    send_from_directory,
    request,
    session
)
from web.routes.dashboard_reservas import dashboard_reservas_bp
from web.routes.dashboard_resenas import dashboard_resenas_bp
from web.routes.dashboard_menu import dashboard_menu_bp
from web.routes.dashboard_usuarios import dashboard_usuarios_bp
from web.routes.landing import landing_bp


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
API_URL = os.getenv("API_URL", "http://localhost:5000/api")
SECRET_KEY = os.getenv("SECRET_KEY", "basheros123")

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.secret_key = SECRET_KEY

app.register_blueprint(dashboard_reservas_bp)
app.register_blueprint(dashboard_resenas_bp)
app.register_blueprint(dashboard_menu_bp)
app.register_blueprint(dashboard_usuarios_bp)
app.register_blueprint(landing_bp)

@app.route("/uploads/<path:filename>")
def uploads(filename):
    ruta = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    if not os.path.exists(ruta):
        return "", 204

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )



@app.route('/dashboard')
@login_requerido
def dashboard_home():
    response = requests.get(f"{API_URL}/stats")
    stats = response.json()

    return render_template(
        "dashboard-home.html",
        stats=stats
    )

@app.route('/dashboard/login', methods=['GET', 'POST'])
def dashboard_login():
    if request.method == 'GET':
        return render_template('dashboard-login.html')

    email = request.form.get('email')
    contrasena = request.form.get('contraseña')

    respuesta = requests.post(
        f'{API_URL}/usuarios/login',
        json={
            'email': email,
            'contrasena': contrasena
        }
    )

    if respuesta.status_code != 200:
        return redirect(url_for('dashboard_login'))

    datos = respuesta.json()
    session['usuario_id'] = datos['usuario_id']
    session['rol'] = datos['rol']
    
    try:
        resp_usuario = requests.get(f"{API_URL}/usuarios/{datos['usuario_id']}", timeout=5)
        if resp_usuario.status_code == 200:
            usuario_data = resp_usuario.json()
            session['nombre'] = usuario_data.get('nombre_usuario', '')
    except requests.exceptions.RequestException:
        session['nombre'] = '' 

    return redirect('/dashboard')

@app.route('/dashboard/logout')
def logout():
    session.clear()
    return redirect('/dashboard/login')


    
# para el route de dashboard 
@app.context_processor
def inject_usuario_dashboard():
    return {
        'usuario_actual': {
            'nombre': session.get('nombre'),
            'rol': session.get('rol')
        }
    }

# @app.route('/dashboard/usuarios/credenciales', methods=['POST'])
# def obtener_credenciales():
#     email = request.form.get('email')
#     try:
#         url_api = 'http://localhost:5000/api/usuarios/credenciales'
#         response = requests.post(url_api, json={'email': email}, timeout=5)
#         response.raise_for_status()
#         credenciales = response.json()
#         flash(f"Credenciales encontradas: {credenciales}")
#     except requests.exceptions.RequestException:
#         flash("Error al obtener las credenciales")
#     return redirect(url_for('dashboard_usuarios'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error-not-found.html'),404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
