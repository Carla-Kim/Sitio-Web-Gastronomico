import os
import sys
from flask import Flask, render_template
from api.app import app as api_app

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

@app.route('/')
def index():
    return render_template('inicio.html')
    

@app.route('/login')
def login():
    # hay que agregar lógica para manejar el inicio de sesión, validación de usuarios, etc. antes de mostrar esta página
    return render_template('login.html')

@app.route('/admin')
def admin_panel():
    # hay que agregar lógica para verificar si el usuario es admin o un usuario válido antes de mostrar esta página
    return render_template('admin.html')

@app.route('/resenas')
def resenas():
    return render_template('resenas.html')

@app.route('/reservas')
def reservas():
    return render_template('reservas.html')

@app.route('/menu')
def mostrar_menu():
    with api_app.test_client() as client:
        categorias_resp = client.get('/categorias', query_string={'_limit': 1000, '_offset': 0})
        productos_resp = client.get('/productos', query_string={'_limit': 1000, '_offset': 0})

    if categorias_resp.status_code != 200 or productos_resp.status_code != 200:
        return render_template('menu.html', menu_agrupado=[])

    categorias_data = categorias_resp.get_json().get('data', [])
    productos_data = productos_resp.get_json().get('productos', [])

    menu_agrupado = []
    for categoria in categorias_data:
        productos_filtrados = [p for p in productos_data if p['categoria'] == categoria['categorias_id']]
        menu_agrupado.append({
            'categoria': categoria,
            'productos': productos_filtrados
        })

    return render_template('menu.html', menu_agrupado=menu_agrupado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)