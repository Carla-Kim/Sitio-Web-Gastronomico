import requests
import os
from flask import Flask, render_template, request, redirect, url_for, flash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

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

@app.route('/dashboard')
def dashboard_landing():
    return render_template('dashboard-inicio.html')

@app.route('/dashboard/login')
def dashboard_login():
    return render_template('dashboard-login.html')

@app.route('/dashboard/reservas', methods=['GET', 'POST'])
def dashboard_reservas():
    if request.method == 'POST':
       reserva_a_eliminar = request.form.get('id_reserva')
       if not reserva_a_eliminar:
           flash("No se pudo completar la acción: ID inexistente")
           return redirect(url_for('dashboard_reservas'))
       try:
            url_api = f'http://localhost:5000/reservas/{reserva_a_eliminar}'
            response = requests.delete(url_api, timeout=5)
            response.raise_for_status()
            return redirect(url_for('dashboard_reservas'))
       except requests.exceptions.RequestException as e:
            print(f"Error al eliminar en API: {e}")
            return render_template('error.html'), 500
    else:
       try:
           url_api = 'http://localhost:5000/reservas'
           response = requests.get(url_api, timeout=5)
           response.raise_for_status()
    
           lista_reservas = response.json()
           return render_template('dashboard-reservas.html', reservas=lista_reservas)
       except requests.exceptions.RequestException as e:
           print(f"Error crítico al conectar con la API: {e}")
           return render_template('error-conexion.html'),500 

@app.route('/dashboard/reseñas', methods=['GET', 'POST'])
def dashboard_reseñas():
    if request.method == 'POST':
       reseña_a_eliminar = request.form.get('id_reseña')
       if not reseña_a_eliminar:
           flash("No se pudo completar la acción: ID inexistente")
           return redirect(url_for('dashboard_reseñas'))
       try:
            url_api = f'http://localhost:5000/resenas/{reseña_a_eliminar}'
            response = requests.delete(url_api, timeout=5)
            response.raise_for_status()
            return redirect(url_for('dashboard_reseñas'))
       except requests.exceptions.RequestException as e:
            print(f"Error al eliminar en API: {e}")
            return render_template('error-conexion.html'), 500
    else:
       try:
           url_api = 'http://localhost:5000/resenas'
           response = requests.get(url_api, timeout=5)
           response.raise_for_status()
    
           lista_reseñas = response.json()
           return render_template('dashboard-reseñas.html', reseñas=lista_reseñas)
       except requests.exceptions.RequestException as e:
           print(f"Error crítico al conectar con la API: {e}")
           return render_template('error-conexion.html'),500 

@app.route('/dashboard/menu', methods=['GET', 'POST'])
def dashboard_menu():
    if request.method == 'POST':
       producto_a_eliminar = request.form.get('id_producto')
       if not producto_a_eliminar:
           flash("No se pudo completar la acción: ID inexistente")
           return redirect(url_for('dashboard_menu'))
       try:
            url_api = f'http://localhost:5000/productos/{producto_a_eliminar}'
            response = requests.delete(url_api, timeout=5)
            response.raise_for_status()
            return redirect(url_for('dashboard_menu'))
       except requests.exceptions.RequestException as e:
            print(f"Error al eliminar en API: {e}")
            return render_template('error-conexion.html'), 500
    else:
       try:
           url_api_categorias = 'http://localhost:5000/categorias'
           url_api_productos = 'http://localhost:5000/productos'
           response_categorias = requests.get(url_api_categorias, timeout=5)
           response_categorias.raise_for_status()
           response_productos = requests.get(url_api_productos, timeout=5)
           response_productos.raise_for_status()

           lista_categorias = response_categorias.json()
           lista_productos = response_productos.json()
           return render_template('dashboard-menu.html', productos=lista_productos, categorias=lista_categorias)
       except requests.exceptions.RequestException as e:
           print(f"Error crítico al conectar con la API: {e}")
           return render_template('error-conexion.html'),500

@app.route('/dashboard/usuarios', methods=['GET', 'POST'])
def dashboard_usuarios():
    if request.method == 'POST':
       usuario_a_eliminar = request.form.get('id_usuario')
       if not usuario_a_eliminar:
           flash("No se pudo completar la acción: ID inexistente")
           return redirect(url_for('dashboard_usuarios'))
       try:
            url_api = f'http://localhost:5000/usuarios/{usuario_a_eliminar}'
            response = requests.delete(url_api, timeout=5)
            response.raise_for_status()
            return redirect(url_for('dashboard_usuarios'))
       except requests.exceptions.RequestException as e:
            print(f"Error al eliminar en API: {e}")
            return render_template('error-conexion.html'), 500
    else:
       try:
           url_api = 'http://localhost:5000/usuarios'
           response = requests.get(url_api, timeout=5)
           response.raise_for_status()
    
           lista_usuarios = response.json()
           return render_template('dashboard-usuarios.html', usuarios=lista_usuarios)
       except requests.exceptions.RequestException as e:
           print(f"Error crítico al conectar con la API: {e}")
           return render_template('error-conexion.html'),500 
       
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error-not-found.html'),404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)