import requests
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from api.database import categorias, menu

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.secret_key = 'clave-secreta'

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

@app.route('/reservas', methods=['GET', 'POST'])
def reservas():
    try:
        resp = requests.get('http://localhost:5000/api/servicios')
        servicios = resp.json().get('data', []) if resp.status_code == 200 else []
    except:
        servicios = []
    
    if request.method == 'POST':
        nombre_completo = request.form.get('nombre', '').split(' ', 1)
        nombre = nombre_completo[0]
        apellido = nombre_completo[1] if len(nombre_completo) > 1 else ''

        data = {
            "cantidad_personas": int(request.form.get('comensales')),
            "fecha": request.form.get('fecha'),
            "servicio_ID": 1, #Servicio_id deberia ser null o no estar en la db ya que esto lo maneja servicio_reserva_id
            "nombre": nombre,
            "apellido": apellido,
            "email": request.form.get('email'),
            "DNI": request.form.get('documento'),
            "telefono": request.form.get('telefono'),
        }

        try:
            response = requests.post('http://localhost:5000/api/reservas', json=data)

            if response.status_code == 201:
                reserva_id = response.json().get('reserva_id')
                serv_seleccionados = request.form.getlist('servicios')

                if serv_seleccionados and reserva_id:
                    requests.put(f'http://localhost:5000/api/servicios-reservas/{reserva_id}', json ={"servicios_id": [int(s) for s in serv_seleccionados]}
                    )
                flash('Se realizó la reserva con exito.', 'success')
                return redirect(url_for('reservas'))
            else:
                error_msg = response.json().get('errors', [{}])[0].get('message', 'Ha ocurrido un error inesperado')
                flash(error_msg, 'error')
        
        except Exception as e:
            print(f"Error al conectar con la API: {e}")
            flash('Error de conexión.', 'error')

    return render_template('reservas.html', servicios=servicios)

@app.route('/menu')
def mostrar_menu():
    todas_las_categorias = categorias.query.all() 
    todos_los_productos = menu.query.all()
    
    menu_agrupado = []
    for cat in todas_las_categorias:
        prod_filtrados = [p for p in todos_los_productos if p.categorias_id == cat.categorias_id]
        menu_agrupado.append((cat, prod_filtrados))
        
    return render_template('menu.html', menu_agrupado=menu_agrupado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)