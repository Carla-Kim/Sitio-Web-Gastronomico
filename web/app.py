import requests
import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash
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

@app.route('/menu', endpoint='menu')
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

@app.route('/resenas')
def resenas():       
    limit = request.args.get('limit', default=5, type=int)
    offset = request.args.get('offset', default=0, type=int)
    
    with api_app.test_client() as client:
        # Obtener reseñas paginadas
        resenas_resp = client.get('/resenas', query_string={'limit': limit, 'offset': offset})
        # Obtener promedios
        promedio_ambiente_resp = client.get('/resenas/promedio/ambiente')
        promedio_comida_resp = client.get('/resenas/promedio/comida')
        promedio_servicio_resp = client.get('/resenas/promedio/servicio')
    
    resenas_list = []
    total_resenas = 0
    promedio_ambiente = 0
    promedio_comida = 0
    promedio_servicio = 0
    
    # Procesar reseñas
    if resenas_resp.status_code == 200:
        resenas_data = resenas_resp.get_json()
        resenas_list = resenas_data.get('resenas', [])
        total_resenas = resenas_data.get('total', 0)
    
    # Procesar promedios
    if promedio_ambiente_resp.status_code == 200:
        promedio_ambiente = promedio_ambiente_resp.get_json().get('promedio', 0)
    if promedio_comida_resp.status_code == 200:
        promedio_comida = promedio_comida_resp.get_json().get('promedio', 0)
    if promedio_servicio_resp.status_code == 200:
        promedio_servicio = promedio_servicio_resp.get_json().get('promedio', 0)
    
    # Calcular paginación
    total_paginas = (total_resenas + limit - 1) // limit if total_resenas > 0 else 1
    pagina_actual = (offset // limit) + 1
    
    return render_template('resenas.html', 
                          resenas=resenas_list,
                          promedio_ambiente=promedio_ambiente,
                          promedio_comida=promedio_comida,
                          promedio_servicio=promedio_servicio,
                          limit=limit,
                          offset=offset,
                          total_paginas=total_paginas,
                          pagina_actual=pagina_actual)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)