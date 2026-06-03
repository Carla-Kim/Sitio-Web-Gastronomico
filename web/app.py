import os
from flask import Flask, render_template

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

@app.route('/dashboard/reseñas')
def dashboard_reseñas():
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
    return render_template('dashboard-resenas.html', reseñas=lista_reseñas)

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
    return render_template('dashboard-usuarios.html', usuarios=lista_usuarios)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)