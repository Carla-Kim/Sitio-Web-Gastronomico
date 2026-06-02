import requests
import os
from flask import Flask, render_template, request, redirect, url_for

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

@app.route('/dashboard/reservas')
def dashboard_reservas():
    return render_template('dashboard-reservas.html')

@app.route('/dashboard/reseñas', methods=['GET', 'POST'])
def dashboard_reseñas():
    if request.method == 'POST':
       reseña_a_eliminar = request.form.get('id_reseña')
       try:
            url_api = f'http://localhost:5000/reseñas/eliminar/{reseña_a_eliminar}'
            response = requests.post(url_api, timeout=5)
            response.raise_for_status()
            return redirect(url_for('dashboard_reseñas'))
       except requests.exceptions.RequestException as e:
            print(f"Error al eliminar en API: {e}")
            return render_template('error-conexion.html'), 500
    else:
       try:
           url_api = 'http://localhost:5000/reseñas'
           response = requests.get(url_api, timeout=5)
           response.raise_for_status()
    
           lista_reseñas = response.json()
           return render_template('dashboard-reseñas.html', reseñas=lista_reseñas)
       except requests.exceptions.RequestException as e:
           print(f"Error crítico al conectar con la API: {e}")
           return render_template('error-conexion.html'),500 

@app.route('/dashboard/menu')
def dashboard_menu():
    # logica de verificacion de si el usuario es admin o no.
    # logica para usar los datos de la base de datos.
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
    return render_template('dashboard-menu.html', productos=lista_productos, categorias=lista_categorias)

@app.route('/dashboard/usuarios')
def dashboard_usuarios():
    lista_usuarios = [
        {
            "id": 3,
            "usuario": "Pepe",
            "nombre": "Nicolás",
            "apellido": "West",
            "email": "nwest@fi.uba.ar", 
            "rol": "Admin",
        },
        {
            "id": 2,
            "usuario": "Pepe2",
            "nombre": "Agustín",
            "apellido": "West",
            "email": "nwest@fi.uba.ar", 
            "rol": "Usuario",
        }      
    ] 
    return render_template('dashboard-usuarios.html', usuarios=lista_usuarios)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)