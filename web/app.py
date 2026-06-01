import requests
import os
from functools import wraps
from flask import Flask, render_template, session, redirect, request, url_for, flash
import requests


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
API_URL = "http://localhost:5000/api"

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.secret_key = os.getenv("SECRET_KEY")


# Función de testeo (sin endpoints del backend)
def obtener_json(url, valor_default):
    try:
        respuesta = requests.get(url)

        if respuesta.status_code != 200:
            return valor_default

        return respuesta.json()

    except:
        return valor_default

def usuario_actual():
    usuario_id = session.get("usuario_id")

    if usuario_id is None:
        return None
    
    respuesta = requests.get(
        f'{API_URL}/usuarios/{usuario_id}'
    )

    if respuesta.status_code != 200:
        return None

    return respuesta.json()

def login_requerido(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if usuario_actual() is None:
            return redirect('/dashboard/login')

        return f(*args, **kwargs)

    return wrapper

def admin_requerido(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        usuario = usuario_actual()

        if usuario is None:
            return redirect('/dashboard/login')

        if usuario["rol"] != "admin":
            return redirect('/dashboard')

        return f(*args, **kwargs)

    return wrapper


@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/dashboard')
# @login_requerido
def dashboard_landing():
    return render_template('dashboard-inicio.html')

@app.route('/dashboard/login', methods=['GET', 'POST'])
def dashboard_login():
    if request.method == 'GET':
        return render_template('dashboard-login.html')

    email = request.form['email']
    contraseña = request.form['contraseña']

    respuesta = requests.post(
        f'{API_URL}/login',
        json={
            'email': email,
            'contraseña': contraseña
        }
    )

    if respuesta.status_code != 200:
        return render_template(
            'dashboard-login.html',
            error='Credenciales inválidas'
        )

    datos = respuesta.json()

    session['usuario_id'] = datos['id']

    return redirect('/dashboard')

@app.route('/dashboard/logout')
def logout():
    session.clear()
    return redirect('/dashboard/login')

@app.route('/dashboard/reservas', methods=['GET', 'POST'])
# @login_requerido
def dashboard_reservas():
#    if request.method == 'POST':
#        reserva_a_eliminar = request.form.get('id_reserva')
#        if not reserva_a_eliminar:
#            flash("No se pudo completar la acción: ID inexistente")
#            return redirect(url_for('dashboard_reservas'))
#        try:
#            url_api = f'http://localhost:5000/reservas/{reserva_a_eliminar}'
#            response = requests.delete(url_api, timeout=5)
#            response.raise_for_status()
#            return redirect(url_for('dashboard_reservas'))
#        except requests.exceptions.RequestException as e:
#            print(f"Error al eliminar en API: {e}")
#            return render_template('error.html'), 500
#    else:
#        try:
#            url_api = 'http://localhost:5000/reservas'
#            response = requests.get(url_api, timeout=5)
#            response.raise_for_status()

#            lista_reservas = response.json()
#            return render_template('dashboard-reservas.html', reservas=lista_reservas)
#        except requests.exceptions.RequestException as e:
#            print(f"Error crítico al conectar con la API: {e}")
#            return render_template('error-conexion.html'),500

    lista_reservas = [{
        "id": 1,
        "fecha": "25-05-2026",
        "email": "loremipsum@gmail.com",
        "nombre": "lorem",
        "apellido": "ipsum",
        "dni": 12345678,
        "telefono": "11 1234-5678",
        "servicio": "Estacionamiento",
        "estado": "Finalizado",
        "cantidad": 5
    }]

    lista_servicios = [
        {"id": 1, "nombre": "Estacionamiento"},
        {"id": 2, "nombre": "Silla de ruedas"}
    ]

    return render_template(
        'dashboard-reservas.html',
        reservas=lista_reservas,
        servicios=lista_servicios
    )

@app.route('/dashboard/reseñas', methods=['GET', 'POST'])
# @login_requerido
def dashboard_reseñas():
#    if request.method == 'POST':
#        reseña_a_eliminar = request.form.get('id_reseña')
#        if not reseña_a_eliminar:
#           flash("No se pudo completar la acción: ID inexistente")
#           return redirect(url_for('dashboard_reseñas'))
#        try:
#            url_api = f'http://localhost:5000/resenas/{reseña_a_eliminar}'
#            response = requests.delete(url_api, timeout=5)
#            response.raise_for_status()
#            return redirect(url_for('dashboard_reseñas'))
#        except requests.exceptions.RequestException as e:
#            print(f"Error al eliminar en API: {e}")
#            return render_template('error-conexion.html'), 500
#    else:
#        try:
#            url_api = 'http://localhost:5000/resenas'
#            response = requests.get(url_api, timeout=5)
#            response.raise_for_status()
#    
#            lista_reseñas = response.json()
#            return render_template('dashboard-reseñas.html', reseñas=lista_reseñas)
#        except requests.exceptions.RequestException as e:
#           print(f"Error crítico al conectar con la API: {e}")
#            return render_template('error-conexion.html'),500

    lista_reseñas = [
        {
            "id": 3,
            "id_reserva": 4,
            "nombre": "Nicolás",
            "apellido": "West",
            "comentario": "Muy bueno todo", 
            "ambiente": 4,
            "servicio": 3,
            "comida": 4,
            "fecha": "25-05-2026"
        },   
        {
            "id": 2,
            "id_reserva": 5,
            "nombre": "Agustín",
            "apellido": "West",
            "comentario": "Muy bueno todo", 
            "ambiente": 2,
            "servicio": 1,
            "comida": 5,
            "fecha": "26-05-2026"
        }   
    ] 
    return render_template(
        'dashboard-resenas.html',
        reseñas=lista_reseñas
    )

@app.route('/dashboard/menu', methods=['GET', 'POST'])
# @login_requerido
def dashboard_menu():
#    if request.method == 'POST':
#       producto_a_eliminar = request.form.get('id_producto')
#       if not producto_a_eliminar:
#           flash("No se pudo completar la acción: ID inexistente")
#           return redirect(url_for('dashboard_menu'))
#       try:
#            url_api = f'http://localhost:5000/productos/{producto_a_eliminar}'
#            response = requests.delete(url_api, timeout=5)
#            response.raise_for_status()
#            return redirect(url_for('dashboard_menu'))
#       except requests.exceptions.RequestException as e:
#            print(f"Error al eliminar en API: {e}")
#            return render_template('error-conexion.html'), 500
#    else:
#       try:
#           url_api_categorias = 'http://localhost:5000/categorias'
#           url_api_productos = 'http://localhost:5000/productos'
#           response_categorias = requests.get(url_api_categorias, timeout=5)
#           response_categorias.raise_for_status()
#           response_productos = requests.get(url_api_productos, timeout=5)
#           response_productos.raise_for_status()
#
#           lista_categorias = response_categorias.json()
#           lista_productos = response_productos.json()
#           return render_template('dashboard-menu.html', productos=lista_productos, categorias=lista_categorias)
#       except requests.exceptions.RequestException as e:
#           print(f"Error crítico al conectar con la API: {e}")
#           return render_template('error-conexion.html'),500

    lista_productos = [
        {
            "id": 1, 
            "nombre": "Milanesa con Papas Fritas", 
            "categoria": "Platos Principales", 
            "precio": 4500, 
            "descripcion": "Milanesa de carne vacuna acompañada de papas fritas bastón."
        },
        {
            "id": 2, 
            "nombre": "Empanada de Carne", 
            "categoria": "Entradas", 
            "precio": 800, 
            "descripcion": "Empanada criolla frita, cortada a cuchillo."
        },
        {
            "id": 3, 
            "nombre": "Volcán de Chocolate", 
            "categoria": "Postres", 
            "precio": 2200, 
            "descripcion": "Bizcocho tibio con corazón de chocolate fundido y helado."
        }   
    ]
    lista_categorias = [
        {"id": 1, "nombre": "Platos principales"},
        {"id": 2, "nombre": "Bebidas"},
        {"id": 3, "nombre": "Entradas"}
    ]
    return render_template(
        'dashboard-menu.html',
        productos=lista_productos,
        categorias=lista_categorias
    )

@app.route('/dashboard/usuarios', methods=['GET', 'POST'])
# @login_requerido
def dashboard_usuarios():
#    if request.method == 'POST':
#        usuario_a_eliminar = request.form.get('id_usuario')
#        if not usuario_a_eliminar:
#            flash("No se pudo completar la acción: ID inexistente")
#            return redirect(url_for('dashboard_usuarios'))
#        try:
#            url_api = f'http://localhost:5000/usuarios/{usuario_a_eliminar}'
#            response = requests.delete(url_api, timeout=5)
#            response.raise_for_status()
#            return redirect(url_for('dashboard_usuarios'))
#        except requests.exceptions.RequestException as e:
#            print(f"Error al eliminar en API: {e}")
#            return render_template('error-conexion.html'), 500
#    else:
#        try:
#            url_api = 'http://localhost:5000/usuarios'
#            response = requests.get(url_api, timeout=5)
#            response.raise_for_status()
#    
#            lista_usuarios = response.json()
#            return render_template('dashboard-usuarios.html', usuarios=lista_usuarios)
#        except requests.exceptions.RequestException as e:
#            print(f"Error crítico al conectar con la API: {e}")
#            return render_template('error-conexion.html'),500     

    lista_usuarios = [
        {
            "id": 3,
            "usuario": "Pepe",
            "nombre": "Nicolás",
            "apellido": "West",
            "email": "nwest@fi.uba.ar", 
            "rol": "admin",
        },
        {
            "id": 2,
            "usuario": "Pepe2",
            "nombre": "Agustín",
            "apellido": "West",
            "email": "nwest@fi.uba.ar", 
            "rol": "usuario",
        }      
    ] 
    return render_template(
        'dashboard-usuarios.html',
        usuarios=lista_usuarios
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
